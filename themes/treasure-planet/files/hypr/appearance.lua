hl.config({
    general = {
        gaps_in = 5,
        gaps_out = 14,
        border_size = 2,
        col = {
            active_border = { colors = { "rgba(7fe3efff)", "rgba(b9cdd2ff)" }, angle = 45 },
            inactive_border = "rgba(34586aaa)",
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
            color = 0x660e2230,
        },
        blur = { enabled = false, size = 3, passes = 1 },
    },
})
