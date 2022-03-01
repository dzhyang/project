

using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace DzhYang.Shared.HotLoadComponent.Controllers;

[Route("[controller]/[action]")]
[ApiController]
public class HlcController : ControllerBase
{
    private readonly ILogger<HlcController> _logger;
    private readonly HotLoadComponentManager _manager;

    public HlcController(HotLoadComponentManager manager, ILogger<HlcController> logger)
    {
        _manager = manager;
        _logger = logger;
    }
    [HttpPost]
    public string Add([FromForm]HotLoadComponent hlc)
    {
        _logger.LogInformation("Adding");
        var rt = _manager.Add("HotLoadComponentLib", "描述", new("1.2.3.45"));
        return rt.state.ToString();
    }

    [HttpPost]
    public string Update()
    {
        _logger.LogInformation("Updateing");
        var rt = _manager.Update("HotLoadComponentLib", "change");
        return _manager[("HotLoadComponentLib", new("1.2.3.45"))]!.Description;
    }

    [HttpDelete]
    public string Remove(int id)
    {
        _logger.LogInformation("Removeing");
        var rt = _manager.Remove("HotLoadComponentLib", new("1.2.3.45"));
        return rt.state.ToString();
    }
}
