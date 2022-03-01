using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DzhYang.Shared.HotLoadComponent;

public class HotLoadComponentOption
{
    public string HotLoadComponentPath { get; set; } = "HotLoadComponent";

    public bool IsDeleteWhenUninstalled { get; set; } = true;
    public List<string> NotCacheNamespaceSegment { get; set; } = new();
}
