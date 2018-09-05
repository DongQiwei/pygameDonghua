import math
def collide_check(item,target):
    col_balls = []
    for each in target:
        distance = math.sqrt(
            math.pow((item.rect.center[0] - each.rect.center[0]),2)
            + math.pow((item.rect.center[1] - each.rect.center[1]),2))
        if distance <= (item.rect.width + each.rect.width)/2:
            col_balls.append(each)
    return col_balls

