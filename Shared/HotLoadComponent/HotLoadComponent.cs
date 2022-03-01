using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using DzhYang.Shared.HotLoadComponent.Abstractions;
namespace DzhYang.Shared.HotLoadComponent;
 
public record HotLoadComponent(string Name,string Description,Version Version);