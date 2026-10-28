hl.config({
    general = {
        gaps_in = 5,
        gaps_out = 14,
        border_size = 2,
        col = {
            active_border = { colors = { "rgba(f0a84aff)", "rgba(c47a3aff)" }, angle = 45 },
            inactive_border = "rgba(4a3429aa)",
        },
        resize_on_border = false,
        allow_tearing = false,
        layout = "dwindle",
    },
    decoration = {
        rounding = 6,
        rounding_power = 2,
        active_opacity = 1.0,
        inactive_opacity = 1.0,
        shadow = {
            enabled = false,
            range = 0,
            render_power = 3,
            color = 0x66140f12,
        },
        blur = { enabled = false, size = 3, passes = 1 },
    },
})
