using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Microsoft.AspNetCore.Mvc.Infrastructure;
using Microsoft.Extensions.Primitives;

namespace DzhYang.Shared.HotLoadComponent;

internal class DescriptorChangeProvider : IActionDescriptorChangeProvider
{
    private CancellationTokenSource _tokenSource = new();
    public IChangeToken GetChangeToken()
    {
        return new CancellationChangeToken(_tokenSource.Token);
    }

    public void Cancel()
    {
        var oldtokenSource = _tokenSource;
        _tokenSource = new();
        oldtokenSource.Cancel();
    }
}
