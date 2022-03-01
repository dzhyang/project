using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Runtime.Loader;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;

using Microsoft.Extensions.Logging;

namespace DzhYang.Shared.HotLoadComponent;

internal class HotLoadComponentLoader : AssemblyLoadContext
{
#pragma warning disable CA1416
    private AssemblyDependencyResolver _resolver;
    private ILogger<HotLoadComponentLoader> _logger;

    private HotLoadComponentManager _manager;
    public HotLoadComponentLoader(string pluginPath,HotLoadComponent component, HotLoadComponentManager manager, ILogger<HotLoadComponentLoader> logger)
        : base($"{component.Name}V{component.Version}",isCollectible: true)
    {
        _resolver = new(pluginPath);
        _manager = manager;
        _logger = logger;
    }

    protected override Assembly? Load(AssemblyName assemblyName)
    {
        var assemblyPath = _resolver.ResolveAssemblyToPath(assemblyName);
        if (assemblyPath is not null)//deps.json文件可以解析出来的路径
        {
            //TODO 需要解决共享库版本不一致，（初步想法是在option里设置加载到默认上下文的版本 （还要考虑共享库更新 麻了:(
            //？增加一个Root加载上下文
            string name = assemblyName.Name!;
            if (_manager.Option.NotCacheNamespaceSegment.Any(segment => name.StartsWith(segment)))
            {
                //加载到默认环境
                return Default.LoadFromAssemblyPath(assemblyPath);
            }
            _logger.LogDebug("load {assemblyName} into {componentName}", assemblyName,Name);
            return LoadFromAssemblyPath(assemblyPath);
        }
        return null;
    }

#pragma warning restore CA1416
}
