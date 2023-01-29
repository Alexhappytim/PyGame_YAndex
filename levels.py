levels_dict = {
    1: ["Бегай быстрее!", "player_group.sprites()[0].speed += 1"],
    2: ["Перезаряжай быстрее!",
        "player_group.sprites()[0].gun.reload_delay_par = max(player_group.sprites()[0].gun.reload_delay_par-10,10)"],
    3: ["Шмаляй быстрее!",
        "player_group.sprites()[0].gun.delay_par = max(player_group.sprites()[0].gun.delay_par-1,1)"],
    4: ["Стреляй кучнее!", "player_group.sprites()[0].gun.spread = max(player_group.sprites()[0].gun.spread-2,0)"],
    5: ["Стреляй больнее!", "player_group.sprites()[0].gun.attack += 1"],
    6: ["Стреляй больше!", "player_group.sprites()[0].gun.clip_max += 4"],
    7: ["Живи дольше!", "player_group.sprites()[0].max_health += 10"],
    8: ["Да давайте просто похилимся", "player_group.sprites()[0].health = min(player_group.sprites()[0].max_health, player_group.sprites()[0].health + 30)"],
}
