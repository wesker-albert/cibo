from tests.conftest import WorldFactory


class TestWorld(WorldFactory):
    def test_motd(self):
        assert (
            self.world.motd
            == "━━━━━━[red]┏┓[/]━━━━━━\n━━━━━━[red]┃┃[/]━━━━━━\n[red]┏━━┓┏┓┃┗━┓┏━━┓\n┃┏━┛┣┫┃┏┓┃┃┏┓┃\n┃┗━┓┃┃┃┗┛┃┃┗┛┃\n┗━━┛┗┛┗━━┛┗━━┛[/]\n━━━━━━━━━━━━━━\n━━━━━━━━━━━━━━"
        )
