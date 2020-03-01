tools = ["spoon", "spatula", "tongs", "whisk", "rolling pin", "food processor", "mixer", "scale", "pan", "skillet",
         "pot", "colander", "strainer", "cutting board", "chef's knife", "pairing knife", "bread knife",
         "measuring cups", "peeler", "honing steel", "grater", "ladle", "skimmer", "thermometer", "timer",
         "zester", "chopper", "bowl", "can opener", "jar opener"]


def get_tools(steps):
    used_tools = []
    for step in steps:
        tools_in_step = [tool if tool in step.lower() else None for tool in tools]
        if any(tools_in_step):
            for tool in tools_in_step:
                if tool and tool not in used_tools:
                    used_tools.append(tool)
    return used_tools
