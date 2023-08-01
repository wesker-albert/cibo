from cibo.resources.world import World


def test_motd():
    world = World()

    assert (
        world.motd
        == "━━━━━━[red]┏┓[/]━━━━━━\n━━━━━━[red]┃┃[/]━━━━━━\n[red]┏━━┓┏┓┃┗━┓┏━━┓\n┃┏━┛┣┫┃┏┓┃┃┏┓┃\n┃┗━┓┃┃┃┗┛┃┃┗┛┃\n┗━━┛┗┛┗━━┛┗━━┛[/]\n━━━━━━━━━━━━━━\n━━━━━━━━━━━━━━"
    )
