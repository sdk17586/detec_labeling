import tkinter as tk
from PIL import Image, ImageTk
import os
import json

class ObjectDetectionLabelingTool:
    def __init__(self, root, image_paths, label_dir):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.image_paths = image_paths
        self.label_dir = label_dir
        self.current_image_index = 0
        self.load_current_image()

        self.rectangles = []
        self.current_class = "default_class"

        self.canvas.bind("<Button-1>", self.start_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.end_rectangle)

        self.class_label = tk.Label(root, text="Class:")
        self.class_label.pack()
        self.class_entry = tk.Entry(root, width=20)
        self.class_entry.pack()

        self.save_button = tk.Button(root, text="Save", command=self.save_annotations)
        self.save_button.pack()
        self.next_button = tk.Button(root, text="Next Image (Right Arrow)", command=self.next_image)
        self.next_button.pack()
        self.prev_button = tk.Button(root, text="Previous Image (Left Arrow)", command=self.prev_image)
        self.prev_button.pack()

        root.bind("<Right>", self.next_image)
        root.bind("<Left>", self.prev_image)

    def load_current_image(self):
        self.clear_rectangles()
        image_path = self.image_paths[self.current_image_index]
        pil_image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(pil_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def start_rectangle(self, event):
        self.start_x, self.start_y = event.x, event.y

    def end_rectangle(self, event):
        end_x, end_y = event.x, event.y
        rect = (self.start_x, self.start_y, end_x, end_y)
        self.rectangles.append((rect, self.current_class))
        self.draw_rectangle(rect)

    def draw_rectangle(self, rect):
        self.canvas.create_rectangle(rect, outline="red", width=2)

    def clear_rectangles(self):
        self.rectangles = []
        self.canvas.delete("all")

    def save_annotations(self):
        self.current_class = self.class_entry.get() or "default_class"
        save_path = os.path.join(self.label_dir, os.path.splitext(os.path.basename(self.image_paths[self.current_image_index]))[0] + ".dat")
        class_id = hash(self.current_class) % 100000
        position_list = []
        for rect, _ in self.rectangles:
            position_list.extend([{"x": rect[0], "y": rect[1]}, {"x": rect[2], "y": rect[3]}])

        class_data = {
            "classId": str(class_id),
            "className": self.current_class,
            "color": "#e27c80",
            "cursor": "isPolygon",
            "needCount": -1,
            "position": position_list,
            "showTf": True
        }
        data = {"polygonData": [class_data], "brushData": [], "totalClass": [self.current_class]}
        with open(save_path, 'w') as json_file:
            json.dump(data, json_file)
        print("Annotations saved to", save_path)


    def next_image(self, event=None):
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.load_current_image()
            self.current_class = self.class_entry.get() or "default_class"

    def prev_image(self, event=None):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_current_image()
            self.current_class = self.class_entry.get() or "default_class"

def main():
    root = tk.Tk()
    root.title("Object Detection Labeling Tool")
    image_folder = "/root/labe_ws/ob/resize_data/resize_drink"
    label_dir = "/root/labe_ws/ob/label_info"  
    image_paths = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.endswith(".jpg")]

    app = ObjectDetectionLabelingTool(root, image_paths, label_dir)
    root.mainloop()

if __name__ == "__main__":
    main()
