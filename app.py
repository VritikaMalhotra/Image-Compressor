from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt
import PIL
from PIL import Image
import os, sys

#To run the code comment it and to create .exe uncomment it.
os.chdir(sys._MEIPASS)

#Here we have initialised the window elements in the constrcutor such as width , height etc.
#After that we have called the method inituI fromt he constructor to initialise the windows with the elements.
#We use setWindowTitle ans setGeometry to set the window.
#We then create an object of the class and use the window.

#Using QMainWindow instead of QWidget because it does not allow us to make the staus bar but QMainWindow does.

class App(QMainWindow):

    #Initialising thw window elements.
    def __init__(self):
        super().__init__()
        self.title = 'Image Compressor'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 600
        self.statusBar().showMessage("Message:")
        self.statusBar().setObjectName("status")
        self.image_width = 0
        self.setFixedSize(self.width,self.height) #Setting the size fixed so that changing the size is disabled.

        #NOTE
        # like css , python qt provides qtss which almost follows all commands same as css to apply styling.
        #For that you need to make a file like design.qss(.qss extension)

        self.setObjectName("mainWindow")

        #Reading the stylesheet in the same way as we read the normal file.
        with open("design.qss", "r") as f:
            stylesheet = f.read()

        #As this stylesheet is set in constructer we do not need to read it again.
        self.setStyleSheet(stylesheet)
        self.initUI()

    #Setting window elements.
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    #-----------------------------------------Main Window----------------------------------------------------------
        #Creating frame signgle bubble(For single image)
        self.single_bubble =QFrame(self)
        self.single_bubble.setObjectName("Bubble")
        self.single_bubble.move(50, 100) #At a distance of 50px from xAxis and 100Px from YAxis of window
        self.single_bubble.mousePressEvent = self.single_bubble_clicked

        #Creating heading for single bubble
        self.single_bubble_heading = QLabel(self.single_bubble)
        self.single_bubble_heading.move(93,8) #93px from left of single_bubble frame and 8px from top
        self.single_bubble_heading.setText("Compress Image")
        self.single_bubble_heading.setObjectName("BubbleHeading")

        #Code for writing description in single bubble
        self.single_bubble_paragraph = QLabel(self.single_bubble)
        self.single_bubble_paragraph.move(55,40)
        self.single_bubble_paragraph.setText("Click here to compress single image.")
        self.single_bubble_paragraph.setObjectName("BubbleParagraph")

        # Creating frame Directory bubble
        self.dir_bubble = QFrame(self)
        self.dir_bubble.setObjectName("Bubble")
        self.dir_bubble.move(50, 275)
        self.dir_bubble.mousePressEvent = self.dir_bubble_clicked

        #Heading for directory bubble
        self.dir_bubble_heading = QLabel(self.dir_bubble)
        self.dir_bubble_heading.move(55, 8)
        self.dir_bubble_heading.setText("Compress Multiple Images")
        self.dir_bubble_heading.setObjectName("BubbleHeading")

        #Code for writing description in directory bubble.
        self.dir_bubble_paragraph = QLabel(self.dir_bubble)
        self.dir_bubble_paragraph.move(55, 40)
        self.dir_bubble_paragraph.setWordWrap(True) #When the width is finished it automatically moves to the next line.
        self.dir_bubble_paragraph.setText("Click here to compress multiple images at once.Select the folder and get compressed version of the images in another folder.")
        self.dir_bubble_paragraph.setObjectName("BubbleParagraph")


    #--------------------------------------Single Bubble expanded---------------------------------------------------
        #Frame for expanded single bubble
        self.single_bubble_expanded = QFrame(self)
        self.single_bubble_expanded.setObjectName("BubbleExpanded")
        self.single_bubble_expanded.move(50, 100)
        self.single_bubble_expanded.setVisible(False)

        #Back arrow for expanded single bubble frame
        self.backArraow_single = QLabel(self.single_bubble_expanded)
        self.backArraow_single.move(25,0)
        self.backArraow_single.setTextFormat(Qt.RichText)
        self.backArraow_single.setText("&#8592;")
        self.backArraow_single.setObjectName("BackArrow")
        self.backArraow_single.mousePressEvent = self.back_arrow_clicked

        #Heading in single bubble
        self.single_bubble_heading = QLabel(self.single_bubble_expanded)
        self.single_bubble_heading.move(93, 8)
        self.single_bubble_heading.setText("Compress Image")
        self.single_bubble_heading.setObjectName("BubbleHeading")

        #Select Image
        #Label for select image
        self.select_image_label = QLabel(self.single_bubble_expanded)
        self.select_image_label.move(30, 50)
        self.select_image_label.setText("Choose Image")
        self.select_image_label.setObjectName("BubbleParagraph")

        #LineEdit for entering image path
        self.image_path = QLineEdit(self.single_bubble_expanded)
        self.image_path.setObjectName("PathText")
        self.image_path.move(60,85)

        #Browse button to search locally
        self.browse_button = QPushButton(self.single_bubble_expanded)
        self.browse_button.setText("...")
        self.browse_button.move(240,85)
        self.browse_button.setObjectName("BrowseButton")
        self.browse_button.clicked.connect(self.select_file)

        #Image Quality
        #Label for image quality
        self.select_image_quality = QLabel(self.single_bubble_expanded)
        self.select_image_quality.move(30, 130)
        self.select_image_quality.setText("Choose Quality")
        self.select_image_quality.setObjectName("BubbleParagraph")

        #Line edit for quality path
        self.quality_path = QLineEdit(self.single_bubble_expanded)
        self.quality_path.setObjectName("QualityPathText")
        self.quality_path.move(60, 160)

        #Code to create combo box for quality
        self.quality_combo = QComboBox(self.single_bubble_expanded)
        self.quality_combo.move(170,160)
        self.quality_combo.addItem("High")
        self.quality_combo.addItem("Medium")
        self.quality_combo.addItem("Low")
        self.quality_combo.setObjectName("QualityCombo")
        self.quality_combo.resize(96,20)
        self.quality_combo.currentIndexChanged.connect(self.quality_current_value)

        #Button to compress image
        self.compress_image = QPushButton(self.single_bubble_expanded)
        self.compress_image.setText("Compress")
        self.compress_image.move(115, 260)
        self.compress_image.setObjectName("CompressButton")
        self.compress_image.clicked.connect(self.resize_pic)

    #--------------------------------------End single bubble expanded--------------------------------------------------------

    # --------------------------------------Dir Bubble expanded---------------------------------------------------

        #Code for frame
        self.dir_bubble_expanded = QFrame(self)
        self.dir_bubble_expanded.setObjectName("BubbleExpanded")
        self.dir_bubble_expanded.move(50, 100)
        self.dir_bubble_expanded.setVisible(False)

        #Code for back arrow
        self.backArraow_dir = QLabel(self.dir_bubble_expanded)
        self.backArraow_dir.move(25, 0)
        self.backArraow_dir.setTextFormat(Qt.RichText)
        self.backArraow_dir.setText("&#8592;")
        self.backArraow_dir.setObjectName("BackArrow")
        self.backArraow_dir.mousePressEvent = self.back_arrow_clicked

        #Code for heading
        self.dir_bubble_heading = QLabel(self.dir_bubble_expanded)
        self.dir_bubble_heading.move(80, 8)  # 110 from left of single_bubble frame and 8px from top
        self.dir_bubble_heading.setText("Compress Multiple Image")
        self.dir_bubble_heading.setObjectName("BubbleHeading")


        #Choose Source Directory
        #Label for choose source directory
        self.select_source_label = QLabel(self.dir_bubble_expanded)
        self.select_source_label.move(30, 50)  # 110 from left of single_bubble frame and 8px from top
        self.select_source_label.setText("Choose Source Directory")
        self.select_source_label.setObjectName("BubbleParagraph")

        #Edit text for choose Source directory
        self.source_path = QLineEdit(self.dir_bubble_expanded)
        self.source_path.setObjectName("PathText")
        self.source_path.move(60, 85)

        #Browse button for choose source directory
        self.browse_source_button = QPushButton(self.dir_bubble_expanded)
        self.browse_source_button.setText("...")
        self.browse_source_button.move(240, 85)
        self.browse_source_button.setObjectName("BrowseButton")
        self.browse_source_button.clicked.connect(self.select_folder)

        #Choose Destination directory
        #Label for choose destination directory
        self.select_dest_label = QLabel(self.dir_bubble_expanded)
        self.select_dest_label.move(30, 130)  # 110 from left of single_bubble frame and 8px from top
        self.select_dest_label.setText("Choose Destination Directory")
        self.select_dest_label.setObjectName("BubbleParagraph")

        #Edit text for Choose DEstination directory
        self.dest_path = QLineEdit(self.dir_bubble_expanded)
        self.dest_path.setObjectName("PathText")
        self.dest_path.move(60, 160)

        #Browse button for choose destination directory
        self.browse_dest_button = QPushButton(self.dir_bubble_expanded)
        self.browse_dest_button.setText("...")
        self.browse_dest_button.move(240, 160)
        self.browse_dest_button.setObjectName("BrowseButtonDirectory")
        self.browse_dest_button.clicked.connect(self.select_folder)

        #Select Image Quality
        #Label for choose Image quality
        self.select_dir_quality = QLabel(self.dir_bubble_expanded)
        self.select_dir_quality.move(30, 210)
        self.select_dir_quality.setText("Choose Quality")
        self.select_dir_quality.setObjectName("BubbleParagraph")

        #Edit text for choose image quality
        self.quality_dir_path = QLineEdit(self.dir_bubble_expanded)
        self.quality_dir_path.setObjectName("QualityPathText")
        self.quality_dir_path.move(60, 240)

        #Combo box for choose Image quality.
        self.quality_dir_combo = QComboBox(self.dir_bubble_expanded)
        self.quality_dir_combo.move(170, 240)
        self.quality_dir_combo.addItem("High")
        self.quality_dir_combo.addItem("Medium")
        self.quality_dir_combo.addItem("Low")
        self.quality_dir_combo.setObjectName("QualityCombo")
        self.quality_dir_combo.resize(96, 20)
        self.quality_dir_combo.currentIndexChanged.connect(self.quality_current_value)

        #Button to compress images in the folder
        self.compress_dir = QPushButton(self.dir_bubble_expanded)
        self.compress_dir.setText("Compress")
        self.compress_dir.move(115, 290)
        self.compress_dir.setObjectName("CompressButton")
        self.compress_dir.clicked.connect(self.resize_folder)

        # --------------------------------------End Dir expanded bubble--------------------------------------------------------


    #--------------------------------------Main Window End----------------------------------------------------------
        #To display the window
        self.show()
    #--------------------------------------Functionality-----------------------------------------------------------
    #NoTE
    #Whenever we will click lft mouse button on signle_bubble this method will be called
    #and event parameter will be passed to it.Hence passing one event parameter is very important.

    #Called using single_bubble
    #To open Expanded single bubble frame
    def single_bubble_clicked(self,event):
        print("Single bubble clicked")
        self.single_bubble.setVisible(False)
        self.dir_bubble.setVisible(False)
        self.single_bubble_expanded.setVisible(True)
        self.dir_bubble_expanded.setVisible(False)

    #Called using dir_bubble
    #To open expanded directory bubble
    def dir_bubble_clicked(self,event):
        print("Dir bubble clicked")
        self.single_bubble.setVisible(False)
        self.dir_bubble.setVisible(False)
        self.dir_bubble_expanded.setVisible(True)
        self.single_bubble_expanded.setVisible(False)

    #Called using backarrow_single and backarrow_dir
    #To open the original home screen from expanded screens.
    def back_arrow_clicked(self,event):
        self.single_bubble.setVisible(True)
        self.dir_bubble.setVisible(True)
        self.single_bubble_expanded.setVisible(False)
        self.dir_bubble_expanded.setVisible(False)

    #Called using browse_button
    #To open file dialog to select image.
    def select_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;JPEG(*.jpeg,*.jpg);;PNG(*.png)", options=options)
        if fileName:
            print(fileName)
            self.image_path.setText(fileName)
            img = Image.open(fileName)
            self.image_width = img.width
            self.quality_path.setText(str(self.image_width))

    #Called using browse_source_button
    #To select the source folder for compression
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")

        if('BrowseButtonDirectory' in self.sender().objectName()):
            print('Directory Button Clicked')
            self.dest_path.setText(folder)
        else:
            print("Source Button Clicked")
            self.source_path.setText(folder)

            files = os.listdir(folder)
            print(files)
            first_pic = folder +'/'+ files[0]
            print(first_pic)
            img = Image.open(first_pic)
            self.image_width = img.width
            self.quality_dir_path.setText(str(self.image_width))

    #Called using quality_combo and quality_dir_combo
    #This is used to set the width according to the quality selected for the image compression
    def quality_current_value(self):
        if(self.quality_combo.currentText() == "High"):
            self.quality_path.setText(str(self.image_width))

        if(self.quality_combo.currentText() == "Medium"):
            self.quality_path.setText(str(int(self.image_width / 2)))

        if(self.quality_combo.currentText() == "Low"):
            self.quality_path.setText(str(int(self.image_width / 4)))

        if(self.quality_dir_combo.currentText() == "High"):
            self.quality_dir_path.setText(str(self.image_width))

        if(self.quality_dir_combo.currentText() == "Medium"):
            self.quality_dir_path.setText(str(int(self.image_width / 2)))

        if(self.quality_dir_combo.currentText() == "Low"):
            self.quality_dir_path.setText(str(int(self.image_width / 4)))

    #Called using compress_dir
    #This is used to compress the images in the entire directory and display the percentage of work done.
    def resize_folder(self):
        source_directory = self.source_path.text()
        destination_directory = self.dest_path.text()

        if(source_directory == ""):
            self.statusBar().showMessage("Message: Please select Source directory!")
            return

        if(destination_directory == ""):
            self.statusBar().showMessage("Message: Please select Destination directory!")
            return

        if source_directory == "" or destination_directory == "":
            self.statusBar().showMessage("Message: Please select Source and Destination directory!")
            return

        files = os.listdir(source_directory)
        images_done = 0
        total_images = len(files)
        for file in files:
            images_done = images_done + 1
            if '.jpg' in file or '.png' in file or '.jpeg' in file or '.JPG' in file or '.PNG' in file or '.JPEG' in file:
                old_pic = source_directory + '/' + file
                new_pic = destination_directory + '/' + file
                img = Image.open(old_pic)
                self.image_width = img.width
                self.quality_dir_path.setText(str(self.image_width))
                self.compression_code(old_pic,new_pic,self.image_width)
                print("Done : "+file)
                print('Images done : ',images_done)
                print('Total Images',total_images)
                print("Percentage done : ",(images_done/total_images)*100)
                message = "Message: Compressed "+str(round((images_done/total_images)*100,2))+'%'
                self.statusBar().showMessage(message)
                self.statusBar().repaint()
            else:
                continue
        self.statusBar().showMessage("Message: Compressed")

    #Called using compress_image
    #This is used to compress single image and check wether the picture is in proper format or not.
    def resize_pic(self):

        old_pic = self.image_path.text()
        print(old_pic)
        if '.jpg' not in old_pic and '.png' not in old_pic and '.jpeg' not in old_pic and '.JPG' not in old_pic and '.PNG' not in old_pic and '.JPEG' not in old_pic:
            self.statusBar().showMessage("Message: Please choose an image in proper format!")
            return

        if(old_pic == ""):
            self.statusBar().showMessage("Message: Please choose an image!")
            return

        directories = old_pic.split("/")

        new_pic_name, okPressed = QInputDialog.getText(self, "Save Image as", "Image Name:", QLineEdit.Normal, "")
        if okPressed and new_pic_name != '':
            print(new_pic_name)

        extension = ''

        if('.jpg' in old_pic):
            extension = '.jpg'
        if('.png' in old_pic):
            extension = '.png'
        if('.jpeg' in old_pic):
            extension = '.jpeg'
        if('.JPG' in old_pic):
            extension = '.JPG'
        if('.PNG' in old_pic):
            extension = '.PNG'
        if('.JPEG' in old_pic):
            extension = '.JPEG'

        new_pic_name = new_pic_name + extension

        new_pic = ""
        for directory in directories[:-1]:
            new_pic = new_pic + directory+"/"

        new_pic = new_pic+new_pic_name

        self.compression_code(old_pic,new_pic,int(self.quality_path.text()))
        self.statusBar().showMessage("Message: Compressed")


    #Called from resize_folder and resize_pic
    #Core code used to perform compression
    def compression_code(self, old_pic, new_pic, myWidth):
        try:
            img = Image.open(old_pic)  # Opens up image present at this path.
            wpercent = (myWidth / float(img.size[0]))  # Bascically gettig aspect ratio from width to get correspondign height.
            hsize = int(float(img.size[1] * float(wpercent)))  # New height obtained after using aspect ratio(wpercent)
            img = img.resize((myWidth, hsize), PIL.Image.LANCZOS)
            img.save(new_pic,optimize=True,quality=45)

        except Exception as e:
            self.statusBar().showMessage("Message: "+e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())