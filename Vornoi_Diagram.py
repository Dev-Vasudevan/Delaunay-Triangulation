import matplotlib.pyplot as plt
import numpy as np

class Point :
    def __init__(self, x , y):
        self.x=x
        self.y=y
    def euc_dist (self , p1):
        dis = (self.x - p1.x)**2
        dis += (self.y - p1.y)**2
        return dis**(1/2)
    def __str__(self):
        return f" {self.x},{self.y}"
    def equals(self, other):
        if self.x == other.x and self.y==other.y :
            return True
        return False


class Grid :
    def __init__(self,points,size,accuracy):
        self.points=points
        self.size=size
        self.accuracy=accuracy
        self.triangles=[]

    def get_points(self):
        points = []
        for point in self.points:
            points.append((point.x,point.y))
        return points
class Triangle:
    def __init__(self,vert):
        self.verts=vert
    def get_points(self):
        points =[]
        for point in self.verts:
            points.append((point.x, point.y))
        return points



class Data_Point(Point):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.neighbours =set()
        self.vertices = []
    #     THIS DOESNT MAKES SENSE
    def neighbour (self, Dps):
        # self.neighbours.add(to_values(Dps))
        # print(1)
        # print(self.neighbours)
        # print(2)
        for Dp in Dps:
            for Dp2 in Dps:
                Dp.neighbours.add(Dp2)

def to_values ( points):
    dps = []
    for dp in points :
        dps.append((dp.x,dp.y))
    print(dps)
    return dps


# defining a limited 10x10 grid for points to exist





def closest(grid, grid_point):
    # setting dis to be greater than max distance possible
    dis = grid.size*1.514

    for point in grid.points:
        temp = grid_point.euc_dist(point)
        if dis-grid.accuracy<= temp <= dis+grid.accuracy :
            closest_points.append(point)

        elif temp<dis-grid.accuracy :
            dis=temp

            closest_points=[point]

    return closest_points



def voronoi(grid ) :

    vertices = {}
    # vertex is the key and the value linked to it are the Points that share it
    triangles=[]
    neigh_dp = {}
    # Tuple that the vertex share is the key and the coord of the vertex is the value
    for i in range (int(grid.size*(1/grid.accuracy))):
        for j in range (int(grid.size*(1/grid.accuracy))):

            grid_point = Point(round(i*grid.accuracy,2),round(j*grid.accuracy,2))
            closest_data_points = tuple(closest(grid,grid_point))
            if grid_point.x==4 and grid_point.y==8:
                print(grid_point, end=" :")
                display(closest_data_points)
            # NOW I HAVE A TUPLE OF THE DATA POINTS WHICH ARE CLOSEST TO THE GIVEN GRID POINT
            # IF TEHRE ARE 3 OR MORE DATA POINTS CLOSEST TO THE GRID POINT ITS A VERTEX
            # BY KEEPING TRACK OF THE VERTICES WE CAN CREATE THE VORONOI DIAGRAM

            if len(closest_data_points)>2:
                # print(grid_point,end=" :")
                # display(closest_data_points)
                for t in range (0,len(closest_data_points)-2):
                    triangles.append(Triangle(closest_data_points[t:t+3]))

                # THIS IF STATEMENT IS ADDED AS WE ARE NOT PERFECTLY MEASURING THE DISTANCE BUT THERE IS A SMALL AMOUNT OF ERROR WE HAVE ADDED
                if closest_data_points not in neigh_dp:
                    neigh_dp[closest_data_points]=(grid_point.x,grid_point.y)
                    vertices[(grid_point.x,grid_point.y)]=closest_data_points
                    closest_data_points[0].neighbour(closest_data_points)
                    for dp in closest_data_points:
                        dp.vertices.append((grid_point.x,grid_point.y))

            if len(closest_data_points)==2 and ( grid_point.x== round(grid.size-grid.accuracy ,2) or  grid_point.y == round(grid.size-grid.accuracy ,2) or grid_point.x==0 or  grid_point.y==0 ) :
                #Here i have to CONSIDER THE CASE OF NO VERTEX EVER BEING FORMED AND JUST A STRAIGHT LINE THAT GOES TO INFINITY
                #This now considers the end of grid also as a condition to add a vertex
                # I could add the 2 into one if statement but it would feel verbose
                # print(grid_point.x, grid_point.y,closest_data_points[0],closest_data_points[1])
                # print(grid_point, end=" :")
                # display(closest_data_points)
                if closest_data_points not in neigh_dp:
                    neigh_dp[closest_data_points] = (grid_point.x, grid_point.y)
                    vertices[(grid_point.x, grid_point.y)] = closest_data_points
                    closest_data_points[0].neighbour(closest_data_points)
                    for dp in closest_data_points:
                        dp.vertices.append((grid_point.x, grid_point.y))

    grid.triangles= triangles
    for vertex in vertices:
        print(f"{vertex}:",end="")
        for item in vertices[vertex]:
            print(item,end=" ")
        print()
    print()
    for dp in grid.points:
        print(f"{dp}:", end="")
        for item in dp.neighbours:
            print(item, end=" ")
        print()
    print()
    for dp in grid.points:
        print(f"{dp}:", end="")
        for item in dp.vertices:
            print(item, end=" ")
        print()
    # exit()
    plot_vor(vertices, neigh_dp, grid)

def display(points):
    for point in points:
        print(point,end=" ")
    print(("\n"))
def plot_vor(vertices,neigh_dp,grid):
    print(2)
    fig, ax = plt.subplots()


    # Set limits and display
    ax.set_xlim(0, grid.size)
    ax.set_ylim(0, grid.size)
    for data_point in grid.points:
        print(3)
        # Taking the a vertex at random that belongs to data point
        # and taking the data point which the vertex is shared as the neighbour
        neigh = list(vertices[data_point.vertices[0]])
        neigh.remove(data_point)
        neigh=neigh[0]

        # If it has no edges (points shared by only 2 Data points then every point will be a vertex shared
        # 3 dps hence it will be circular and wont matter which neighbour we start from
        # ordered_vertices = [data_point.vertices[0]]
        # print(ordered_vertices)

        # if there are edges then we must start from there
        for data_points in neigh_dp:
            if len(data_points)==2 and data_point in data_points:
                neigh=list(data_points)
                neigh.remove(data_point)
                neigh=neigh[0]
                data_point.vertices.remove(neigh_dp[data_points])
                data_point.vertices.insert(0,neigh_dp[data_points])
                # ordered_vertices =  [ neigh_dp[data_points]]
                break

        print((vertices.keys()))
        ordered_vertices=[]
        # exit()
        # ordered the vertices
        while len(ordered_vertices)<len(data_point.vertices):

            for vert in data_point.vertices:
                print(len(data_point.vertices))
                # print(vert in ordered_vertices)
                print(f"\n ov:{ordered_vertices} ,  current dp:{data_point}, current neigh:{neigh}, points sharing the {vert} : ",end="")

                display(vertices[vert])
                display(data_point.vertices)
                if vert in ordered_vertices:
                    continue
                if data_point in vertices[vert] and neigh in vertices[vert]:
                    ordered_vertices.append(vert)
                    for item in vertices[vert]:
                        if item != data_point and item !=neigh and item in data_point.neighbours:
                            neigh=item
                            break
                    # break
        # ordered_vertices.append(ordered_vertices[0])
        print(ordered_vertices)
        ov=np.array(ordered_vertices)
        # ov=np.array(data_point.vertices)
        print(data_point, ordered_vertices)


        # plot_triangles(grid.triangles)
        for triangle in grid.triangles:
            verts = triangle.get_points()
            verts.append(verts[0])
            verts = np.array(verts)
            print(len(verts))
            plt.plot(verts.T[0], verts.T[1],color ='black' ,linewidth = '0.5')
        plt.scatter(data_point.x, data_point.y, color='red')

        plt.scatter(ov.T[0], ov.T[1], color="green")
        plt.plot(ov.T[0],ov.T[1])

    plt.show()
    print(1)
    return ()






P1= Data_Point(1,4)
P2 = Data_Point(9,9)
P3 = Data_Point(4,1)
p4= Data_Point(7,4)
p5=Data_Point(5,8)
p6=Data_Point(0.5,0.5)
grid_points = [P1,P2,P3,p4,p5,p6]

grid = Grid(grid_points[:],10,0.1)
voronoi(grid)


