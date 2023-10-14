import cv2
import numpy as np

points = []

class Projection(object):

    def __init__(self, image_path, points):
        """
            :param points: Selected pixels on top view(BEV) image
        """
        if type(image_path) != str:
            self.image = image_path
        else:
            self.image = cv2.imread(image_path)
        self.height, self.width, self.channels = self.image.shape
        self.points = points

    def top_to_front(self, theta=0, phi=0, gamma=0, dx=0, dy=0, dz=0, fov=90):
        """
            Project the top view pixels to the front view pixels.
            :return: New pixels on perspective(front) view image
        """
        ### TODO ###
        np.set_printoptions(precision=3, suppress=True)

        BEV_pixels = []
        BEV_points = []
        FV_points  = []
        FV_pixels  = []
        new_pixels = []
        
        # camera instric
        principal_point = [int(self.height/2),int(self.height/2)]
        print("-----------")
        print("principal point:")
        print(principal_point)
        focal_length = np.tan(np.deg2rad(fov/2))*256
        print("-----------")
        print("focal length:")
        print(focal_length)

        #Convert to principal points coordinate
        for point in self.points:
            pixel_x,pixel_y = principal_point[0]-point[0],principal_point[1]-point[1]
            BEV_pixels.append([pixel_x,pixel_y,1])
        print("-----------")
        print("BEV_pixels:")
        print(BEV_pixels)
        
        #2D to 3D
        #2.5
        for BEV_pixel in BEV_pixels:
            BEV_point = [2.5*BEV_pixel[0]/focal_length,2.5*BEV_pixel[1]/focal_length,1*2.5]
            BEV_points.append(BEV_point)
        BEV_points= np.array(BEV_points)
        print("-----------")
        print("BEV_points:")
        print(BEV_points)
        row_of_ones = np.ones((BEV_points.shape[0],1))
        BEV_points = np.column_stack((BEV_points,row_of_ones))

        # Computing Transform Matrix
        rotation_matrix, _ = cv2.Rodrigues(np.array([np.deg2rad(theta), np.deg2rad(phi), np.deg2rad(gamma)], dtype=np.float32))
        transformation_matrix = np.eye(4)
        transformation_matrix[:3,:3] = rotation_matrix
        transformation_matrix[:3, 3] = [dx,dy,dz]
        print("-----------")
        print("Transform Matrix:")
        print(transformation_matrix)

        #Transform to another camera
        FV_points = np.dot(transformation_matrix, BEV_points.T).T
        FV_points = np.delete(FV_points, -1, axis=1)
        print("-----------")
        print("FV_points:")
        print(FV_points)
        
        #3D to 2D
        for FV_point in FV_points:
            FV_point[0],FV_point[1],FV_point[2] = FV_point[0]/FV_point[2]*focal_length,FV_point[1]/FV_point[2]*focal_length,1
            FV_pixels.append([FV_point[0],FV_point[1],FV_point[2]])
        print("-----------")
        print("FV_pixels")
        print(FV_pixels)
        
        for FV_pixel in FV_pixels:
            new_pixel_x,new_pixel_y = principal_point[0]-int(FV_pixel[0]),principal_point[1]-int(FV_pixel[1])
            new_pixels.append([new_pixel_x,new_pixel_y])
        print("-----------")
        print("new pixel")
        for new_pixel in new_pixels:
            print(new_pixel)

        return new_pixels
    
    def show_image(self, new_pixels, img_name='projection_1.png', color=(0, 0, 255), alpha=0.4):
        """
            Show the projection result and fill the selected area on perspective(front) view image.
        """
        new_image = cv2.fillPoly(
            self.image.copy(), [np.array(new_pixels)], color)
        new_image = cv2.addWeighted(
            new_image, alpha, self.image, (1 - alpha), 0)

        cv2.imshow(f'Top to front view projection {img_name}', new_image)
        cv2.imwrite(img_name, new_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return new_image
#end of class

def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
        points.append([x, y])
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' + str(y), (x+5, y+5), font, 0.5, (0, 0, 255), 1)
        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
        cv2.imshow('image', img)

    # checking for right mouse clicks
    if event == cv2.EVENT_RBUTTONDOWN:
        print(x, ' ', y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' + str(g) + ',' + str(r), (x, y), font, 1, (255, 255, 0), 2)
        cv2.imshow('image', img)

if __name__ == "__main__":

    front_rgb = "bev_data/front1.png"
    top_rgb = "bev_data/bev1.png"

    # click the pixels on window
    img = cv2.imread(top_rgb, 1)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    projection = Projection(front_rgb, points)
    new_pixels = projection.top_to_front(theta=90,dy=1.5)
    projection.show_image(new_pixels)
    cv2.destroyAllWindows()