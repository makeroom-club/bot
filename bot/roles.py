from dataclasses import dataclass


@dataclass
class RoleTemplate:
    name: str
    color: int
    emoji: str


roles = (
    RoleTemplate('linux \U0001F427', 0x9ddc66, '\U0001F427'),
    RoleTemplate('mac \U0001F34F', 0x131f1f, '\U0001F34E'),
    RoleTemplate('windows \U0001F9D1\u200D\U0001F4BB', 0x092553, '\U0001FA9F'),
    RoleTemplate('python', 0x4372a1, '\U0001F40D'),
    RoleTemplate('rust', 0xd5a689, '\U0001F980'),
    RoleTemplate('sql', 0xd88f32, '\U0001F4BE'),
    RoleTemplate('java', 0xa7742f, '\U00002615'),
    RoleTemplate('csharp', 0x3f8324, '#\uFE0F\u20E3'),
    RoleTemplate('typescript/javascript', 0x4278c0, '\U0001F1EF'),
    RoleTemplate('golang', 0x4babd4, '\U0001F1EC'),
    RoleTemplate('ux', 0x546e7a, '\U0001F1FA'),
    RoleTemplate('design', 0xe74c3c, '\U0001F58C'),
    RoleTemplate('mentor', 0xffdf00, '\U0001F3EB'),
)
by_name = {
    template.name: template
    for template in roles
}
by_emoji = {
    template.emoji: template
    for template in roles
}
