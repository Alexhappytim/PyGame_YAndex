levels_dict = {
    1: ["Бегай быстрее!", "player_group.sprites()[0].speed += 1"],
    2: ["Перезаряжай быстрее!",
        "player_group.sprites()[0].gun.reload_delay_par = max(player_group.sprites()[0].gun.reload_delay_par-10,10)"],
    3: ["Шмаляй быстрее!", "player_group.sprites()[0].gun.delay_par = max(player_group.sprites()[0].gun.delay_par-1,1)"]
}
# TODO когда 3 прожата 1, то не шмаляет(
