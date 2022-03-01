using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Loader;
using System.Text;
using System.Threading.Tasks;

using DzhYang.Shared.HotLoadComponent;

using Microsoft.AspNetCore.Mvc.Infrastructure;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.DependencyInjection.Extensions;

namespace DzhYang.Shared.Services;

public static class HotLoadComponentExtensions
{
    public static IServiceCollection AddHotLoadComponent(this IServiceCollection services)
    {

        services.AddSingleton<HotLoadComponentManager>();
        services.TryAddEnumerable(ServiceDescriptor.Singleton<IActionDescriptorChangeProvider, DescriptorChangeProvider>());

        services.Configure<HotLoadComponentOption>(option =>
        {
            option.NotCacheNamespaceSegment.Add("System");
            option.NotCacheNamespaceSegment.Add("Microsoft");
        });

        
        return services;
    }
}
