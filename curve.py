class Curve(object):
    def __init__(self, numbers, lo_bd, up_bd):
        self.numbers = numbers
        self.up_bd = up_bd
        self.lo_bd = lo_bd
        self.steps = (up_bd-lo_bd) // numbers
    
    def seg_initial(self):
        segments = []
        for i in range(self.lo_bd, self.up_bd+self.steps, self.steps):
            segments.append([i, 0])
        self.segments = segments
    
    def seg_update(self, point_1, point_2):
        point_1_x = point_1[0]
        point_1_y = point_1[1]
        point_2_x = point_2[0]
        point_2_y = point_2[1]
        for i in range(self.numbers +1):
            curr = self.segments[i]
            curr_x = curr[0]
            curr_y = curr[1]
            if curr_x <= point_1_x and curr_y <= point_1_y:
                self.segments[i][1] = point_1_y
            elif curr_x >= point_2_x and curr_y >= point_2_y:
                self.segments[i][1] = point_2_y


# curve_1 = Curve(100, 0, 3000)
# curve_1.seg_initial()
# print(curve_1.segments)
# curve_1.seg_update([201,100],[301,50])
# curve_1.seg_update([50,100],[105,50])
# print(curve_1.segments)