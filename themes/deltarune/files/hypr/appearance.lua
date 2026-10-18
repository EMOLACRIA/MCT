hl.config({
    general = {
        gaps_in = 5,
        gaps_out = 14,
        border_size = 2,
        col = {
            active_border = { colors = { "rgba(00d9efff)", "rgba(00a8ebff)" }, angle = 45 },
            inactive_border = "rgba(195a78aa)",
        },
        resize_on_border = false,
        allow_tearing = false,
        layout = "dwindle",
    },
    decoration = {
        rounding = 0,
        rounding_power = 2,
        active_opacity = 1.0,
        inactive_opacity = 1.0,
        shadow = {
            enabled = false,
            range = 0,
            render_power = 3,
            color = 0x660b0c0a,
        },
        blur = { enabled = false, size = 3, passes = 1 },
    },
})
