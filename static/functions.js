let generic_functions = {
    "color": {
        "types": ["run"],
        "color": {
            "default": [1],
            "mode": "single"
        }
    },
    "random": {
        "types": ["run", "animate"],
        "wait_ms": [50],
        "num_value": {
            "label": "Segment Size",
            "default": [60]
        }
    },
    "wipe": {
        "types": ["thread", "run"],
        "color": {
            "default": [2],
            "mode": "single"
        },
        "wait_ms": [50],
        "wait_mode": ["each", "full"],
        "direction": ["left", "right"]
    },
    "single": {
        "types": ["run"],
        "color": {
            "default": [0],
            "mode": "single"
        },
        "num_value": {
            "label": "Pixel id",
            "default": [7]
        },
    },
    "pulse": {
        "types": ["thread", "animate"],
        "color": {
            "default": [4],
            "mode": "single"
        },
        "wait_ms": [25],
        "num_value": {
            "label": "Length",
            "default": [5]
        },
        "wait_mode": ["each", "full"],
        "direction": ["left", "right"],
        "option": {
            "label": "Layer",
            "default": ["True", "False"]
        }
    },
    "chase": {
        "types": ["animate"],
        "color": {
            "default": [3],
            "mode": "single"
        },
        "wait_ms": [50],
        "direction": ["left", "right"],
        "option": {
            "label": "Layer",
            "default": ["True", "False"]
        },
        "num_value": {
            "label": "Interval",
            "default": [3]
        }
    },
    "shift": {
        "types": ["run", "animate"],
        "wait_ms": [0],
        "direction": ["left", "right"],
        "num_value": {
            "label": "Amount",
            "default": [1]
        }
    },
    "rainbowCycle": {
        "types": ["animate"],
        "wait_ms": [50],
        "wait_mode": ["each", "full"],
        "direction": ["left", "right"]
    },
    "rainbowChase": {
        "types": ["animate"],
        "wait_ms": [50],
        "wait_mode": ["each", "full"],
        "direction": ["left", "right"]
    },
    "mix": {
        "types": ["animate", "thread"],
        "color": {
            "default": [[1,2,3]],
            "mode": "multi"
        },
        "wait_ms": [500],
        "wait_mode": ["Blend", "Instant"],
        "option": {
            "label": "Loop to Start",
            "default": ["True", "False"]
        }
    },
    "reverse": {
        "types": ["run"]
    },
    "bounce": {
        "types": ["animate", "thread"],
        "color": {
            "default": [[1,1]],
            "mode": "multi"
        },
        "wait_ms": [20],
        "wait_mode": ["each", "full"],
        "direction": ["left", "right"],
        "num_value": {
            "default": [5],
            "label": "Length"
        }
    }
};
