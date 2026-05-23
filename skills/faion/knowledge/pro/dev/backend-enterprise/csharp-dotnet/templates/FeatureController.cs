// purpose: REST controller skeleton with CancellationToken on every action
// consumes: API contract endpoint list, IUserService interface
// produces: ASP.NET Core controller conforming to cancellation-token-plumbing rule
// depends-on: content/01-core-rules.xml rule cancellation-token-plumbing
// token-budget-impact: ~400 tokens when loaded as context
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace MyApp.Features.Users;

[ApiController]
[Route("api/v1/[controller]")]
[Authorize]
public class UsersController : ControllerBase
{
    private readonly IUserService _userService;
    private readonly ILogger<UsersController> _logger;

    public UsersController(IUserService userService, ILogger<UsersController> logger)
    {
        _userService = userService;
        _logger = logger;
    }

    [HttpGet]
    [ProducesResponseType(typeof(PagedResult<UserDto>), StatusCodes.Status200OK)]
    public async Task<ActionResult<PagedResult<UserDto>>> GetUsers(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20,
        CancellationToken ct = default)
    {
        var result = await _userService.GetAllAsync(page, pageSize, ct);
        return Ok(result);
    }

    [HttpGet("{id:int}")]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<UserDto>> GetUser(int id, CancellationToken ct = default)
    {
        var user = await _userService.GetByIdAsync(id, ct);
        return user is null ? NotFound() : Ok(user);
    }

    [HttpPost]
    [ProducesResponseType(typeof(UserDto), StatusCodes.Status201Created)]
    public async Task<ActionResult<UserDto>> CreateUser(
        CreateUserDto dto, CancellationToken ct = default)
    {
        var user = await _userService.CreateAsync(dto, ct);
        return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user);
    }
}
