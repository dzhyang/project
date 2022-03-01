using System.Collections.Concurrent;
using System.Reflection;

using Microsoft.AspNetCore.Mvc.ApplicationParts;
using Microsoft.AspNetCore.Mvc.Infrastructure;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace DzhYang.Shared.HotLoadComponent;

internal enum OperationType
{
    Add,
    Remove,
    Update
}

/// <summary>
/// 管理热重载组件加载与卸载，
/// </summary>

public class HotLoadComponentManager
{
    private readonly ConcurrentDictionary<HotLoadComponent, WeakReference> _loaders = new();
    private readonly ConcurrentDictionary<string, ConcurrentBag<HotLoadComponent>> _hotLoadComponents = new();
    private readonly IServiceProvider _serviceProvider;
    internal HotLoadComponentOption Option;
    private readonly ApplicationPartManager _partManager;
    private readonly DescriptorChangeProvider _changeProvider;
    private const string HotLoadComponentSuffix = ".dll";

    private readonly string _basePath;

    private static readonly object _lock = new();

    // TODO 只清理指定组件缓存
    private static readonly MethodInfo _clearCache;
    //private static WeakReference _test;
    static HotLoadComponentManager()
    {
        var coreAssembly = AppDomain.CurrentDomain.GetAssemblies().FirstOrDefault(x => x.FullName!.Contains("Microsoft.AspNetCore.Mvc.Core"));
        var propertyHelper = coreAssembly!.GetTypes().FirstOrDefault(x => x.FullName!.Contains("PropertyHelper"));
        _clearCache = propertyHelper!.GetMethod("ClearCache", BindingFlags.Public | BindingFlags.Static)!;
    }
    public HotLoadComponentManager(IOptions<HotLoadComponentOption> option,
                                    ApplicationPartManager partManager,
                                    IEnumerable<IActionDescriptorChangeProvider> changeProviders,
                                    IServiceProvider serviceProvider)
    {
        Option = option.Value;
        _basePath = Path.Combine(Path.GetDirectoryName(Assembly.GetEntryAssembly()!.Location)!, Option.HotLoadComponentPath);
        _partManager = partManager;
        _serviceProvider = serviceProvider;
        _changeProvider = changeProviders.FirstOrDefault(cp => cp is DescriptorChangeProvider) as DescriptorChangeProvider ?? throw new ArgumentException(nameof(changeProviders));


    }
    public HotLoadComponent? this[(string name, Version version) key]
    {
        get
        {
            _hotLoadComponents.TryGetValue(key.name, out var hotLoadComponents);
            return hotLoadComponents?.First(hlc => hlc.Version == key.version);
        }
    }
    public (bool state, string? message) Add(string name, string description, Version version)
    {
        lock (_lock)
        {


            if (_hotLoadComponents.ContainsKey(name))
            {
                _hotLoadComponents.TryGetValue(name, out var hotLoadComponents);
                if (hotLoadComponents!.Any(hlc => hlc.Version == version))
                {
                    return (false, "contains " + name + "V" + version);
                }
            }

            UpdateCollection(name, description, version, OperationType.Add);
            return (true, null);
        }
    }

    public (bool state, string? message) Remove(string name, Version? version)
    {
        lock (_lock)
        {


            if (!_hotLoadComponents.ContainsKey(name))
            {
                return (false, "not contains " + name);
            }
            UpdateCollection(name, null, version, OperationType.Remove);
            return (true, null);
        }
    }
    public (bool state, string? message) Update(string name, string? description = null, Version? oldversion = null, Version? newVersion = null)
    {
        lock (_lock)
        {
            if (!_hotLoadComponents.ContainsKey(name))
            {
                return (false, "not contains " + name);
            }
            if (oldversion is not null)
            {
                if (newVersion is null)
                {
                    return (false, "must give a new version");
                }
                _hotLoadComponents.TryGetValue(name, out var hotLoadComponents);
                if (!hotLoadComponents!.Any(hlc => hlc.Version == oldversion))
                {
                    return (false, "not contains " + name + "V" + oldversion);
                }
            }

            UpdateCollection(name, description, oldversion, OperationType.Update, newVersion);
            return (true, null);
        }
    }
    private void UpdateCollection(string name, string? description, Version? oldversion, OperationType operationType, Version? newVersion = null)
    {
        switch (operationType)
        {
            case OperationType.Add:
                HotLoadComponent hotLoadComponent = new(name, description!, oldversion!);
                InternalAdd(hotLoadComponent);
                break;
            case OperationType.Remove:
                InternalRemove(name, oldversion);
                GC.Collect();
                GC.WaitForPendingFinalizers();
                break;
            case OperationType.Update:
                InternalUpdate(name, description, oldversion);
                break;
        }
    }
    private void InternalAdd(HotLoadComponent hotLoadComponent)//多个不同版本Api可以共存
    {
        //从临时目录加载


        //1.构建路径
        //2.创建loader
        //3.loader缓存
        //4.加入part
        //5.触发更新
        //1.
        string componentFullPath = Path.Combine(_basePath, hotLoadComponent.Name, hotLoadComponent.Version.ToString(), hotLoadComponent.Name + HotLoadComponentSuffix);
        var log = _serviceProvider.GetService<ILogger<HotLoadComponentLoader>>();
        //2.
        var alc = new HotLoadComponentLoader(componentFullPath, hotLoadComponent, this, log!);
        WeakReference reference = new(alc);
        //3.
        _loaders.TryAdd(hotLoadComponent, reference);
        if (_hotLoadComponents.ContainsKey(hotLoadComponent.Name)) _hotLoadComponents[hotLoadComponent.Name].Add(hotLoadComponent);
        else _hotLoadComponents.TryAdd(hotLoadComponent.Name, new() { hotLoadComponent });
        //4.
        _partManager.ApplicationParts.Add(new AssemblyPart(alc.LoadFromAssemblyPath(componentFullPath)));
        //5.
        _changeProvider.Cancel();
    }
    private void InternalRemove(string name, Version? version)
    {
        _hotLoadComponents.TryRemove(name, out var hotLoadComponents);
        if (version is null)//remove all
        {
            foreach (var hcl in hotLoadComponents!)
            {
                //TODO 删除文件
                _loaders.TryRemove(hcl, out var reference);
                var alc = reference!.Target;
                _partManager.ApplicationParts.Remove(_partManager.ApplicationParts.First(part => part.Name == name));
                (alc as HotLoadComponentLoader)!.Unload();
            }
        }
        else
        {
            var hlcsList = hotLoadComponents!.ToList();
            var hlc = hlcsList!.First(hlc => hlc.Version == version);

            //TODO 删除文件
            _loaders.TryRemove(hlc, out var reference);
            var alc = reference!.Target;
            _partManager.ApplicationParts.Remove(_partManager.ApplicationParts.First(part => part.Name == name));
            (alc as HotLoadComponentLoader)!.Unload();

            hlcsList.Remove(hlc);
            if (hlcsList.Count != 0) _hotLoadComponents.TryAdd(name, new(hlcsList!));
        }
        _clearCache.Invoke(null, new object[] { null! });
        _changeProvider.Cancel();
    }
    private void InternalUpdate(string name, string? description = null, Version? oldversion = null, Version? newVersion = null)
    {
        if (oldversion is null)
        {
            if (description is null)
            {
                return;
            }
            else//不会改动文件
            {
                _hotLoadComponents.TryRemove(name, out var hotLoadComponents);
                var hlcsList = hotLoadComponents!.ToList();
                var hlcsUpdateList = hotLoadComponents!.Select(hlc => hlc with { Description = description });
                for (int i = 0; i < hlcsList!.Count; i++)
                {
                    _loaders.TryRemove(hlcsList[i], out var reference);
                    _loaders.TryAdd(hlcsUpdateList.ElementAt(i), reference!);
                }
                _hotLoadComponents.TryAdd(name, new(hlcsUpdateList!));
            }
        }
        else//更新指定版本,先卸载后安装
        {
            _hotLoadComponents.TryGetValue(name, out var hotLoadComponents);
            var hlc = hotLoadComponents!.First(hlc => hlc.Version == oldversion);
            var useDescription = description ?? hlc.Description;
            InternalRemove(name, oldversion);
            GC.Collect();
            GC.WaitForPendingFinalizers();
            InternalAdd(hlc with { Description = useDescription, Version = newVersion! });
        }
    }

}
