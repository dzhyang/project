using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DzhYang.Shared.HotLoadComponent.Abstractions;

public interface IHotloadComponent
{
    string Name { get; }
    string Description { get; }
    Version Version { get; }
}
