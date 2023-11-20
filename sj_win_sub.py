import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, \
    QPushButton, QScrollArea,QFileDialog
from PyQt5 import QtCore
import demo_main as demo
import csv

class MatrixInputWidget(QWidget):
    def __init__(self, rows, cols, name):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.name = name
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.input_fields = []
        self.all_inputs = []
        # 添加行标签
        for row in range(self.rows):
            label = QLabel(f"{self.name}{row + 1}:", self)
            layout.addWidget(label, row + 1, 0)

        # 添加列标签
        for col in range(self.cols):
            label = QLabel(f"{self.name}{col + 1}:", self)
            layout.addWidget(label, 0, col + 1)

        for row in range(self.rows):
            row_inputs = []

            for col in range(self.cols):
                input_field = QLineEdit(self)
                row_inputs.append(input_field)
                layout.addWidget(input_field, row + 1, col + 1)
            self.all_inputs.extend(row_inputs)
            self.input_fields.append(row_inputs)

        self.setLayout(layout)


class MatrixInputApp(QMainWindow):
    matrices = []  # 输入矩阵
    sub_w = []  # 主观权重
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("设计阶段主观权重计算")
        central_widget = QWidget(self)
        # central_widget.resize(592, 629)
        central_widget.resize(592, 629)
        central_widget.setMinimumSize(QtCore.QSize(592, 629))
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 创建一个滚动区域
        scroll_area = QScrollArea(self)
        main_layout.addWidget(scroll_area)

        # 创建一个容纳输入部件的小部件
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)

        content_layout = QVBoxLayout()
        content_widget.setLayout(content_layout)

        matrix_sizes = [(3, 3, 'U'), (7, 7, 'U1'), (3, 3, 'U2'), (4, 4, 'U3')]
        self.matrix_inputs = []


        clean_button = QPushButton("导入外部数据", self)
        clean_button.clicked.connect(self.upload_csv) # 导入表格数据
        content_layout.addWidget(clean_button)

        for rows, cols, name in matrix_sizes:
            matrix_input_widget = MatrixInputWidget(rows, cols, name)
            content_layout.addWidget(matrix_input_widget)
            self.matrix_inputs.append(matrix_input_widget)

        # 给矩阵设置
        convert_button = QPushButton("计算", self)
        convert_button.clicked.connect(self.convert_to_matrices)
        content_layout.addWidget(convert_button)

        clean_button = QPushButton("重置输入", self)
        clean_button.clicked.connect(self.clearAllText)
        content_layout.addWidget(clean_button)


        self.save_button = QPushButton("保存并返回", self)
        content_layout.addWidget(self.save_button)

        self.result_label = QLabel(self)
        content_layout.addWidget(self.result_label)

    def upload_csv(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open CSV File', '', 'CSV Files (*.csv)',options=options)
        if file_name:
            try:
                with open(file_name, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    m1 = []
                    for row in csv_reader:
                        m2 = []
                        for r in row:
                            if r in ['0','1','2']:
                                m2.append(int(r))
                        m1.append(m2)
                    m3 = []
                    m4 = []
                    i = 1
                    while i < len(m1):
                        while m1[i] == []:
                            i += 1
                        if len(m1[i]) != len(m1[i - 1]) and m3 != []:
                            m4.append(m3)
                            m3 = [m1[i]]
                        else:
                            m3.append(m1[i])
                        i += 1
                    m4.append(m3)
                    for i in range(len(self.matrix_inputs)):
                        for j in range(len(self.matrix_inputs[i].input_fields)):
                            for k in range(len(self.matrix_inputs[i].input_fields[j])):
                                self.matrix_inputs[i].input_fields[j][k].setText(str(m4[i][j][k]))

            except Exception as e:
                print(f"Error reading CSV file: {e}")
                return


    def convert_to_matrices(self):
        self.sub_w = []
        self.matrices = []
        flag = 0
        for input_widget in self.matrix_inputs:
            flag += 1
            matrix = []
            for row_inputs in input_widget.input_fields:
                row_data = [input_field.text() for input_field in row_inputs]
                if [] != row_data and '' not in row_data and len(row_data) == len(row_inputs):
                    row_data = (list(map(int, row_data)))
                    matrix.append(row_data)
                else:
                    self.result_label.setText('请完整输入矩阵')
                    return
            self.matrices.append(matrix)
        print('输入比较矩阵为:', self.matrices)  # 输入的矩阵内容

        for mx in self.matrices:
            if mx != [] and len(mx) == len(mx[0]):
                w = demo.Subjective_W(mx)
                if isinstance(w,str):
                    self.result_label.setText("计算错误，请检查矩阵！")
                    return
                else:
                    self.sub_w.extend(w)


        # 权重归一化
        o = 5 if len(self.sub_w) == 25 else 3
        M = [7, 3, 4, 4, 2]
        s = 0
        for i in range(o):
            for j in range(M[i]):
                self.sub_w[o + s] = self.sub_w[i] * self.sub_w[o + s]
                s += 1
        self.sub_w = [round(i,3) for i in self.sub_w]
        if len(self.sub_w) == 17:
            self.result_label.setText("计算成功！")
            print('设计阶段主观权重为:', self.sub_w[3:])

        # 直接赋值，用于测试
        # self.sub_w = [0.172, 0.233, 0.076, 0.391, 0.128, 0.015, 0.244, 0.127, 0.041, 0.427, 0.059, 0.087,
        #               0.258, 0.637, 0.105, 0.41, 0.302, 0.122, 0.166, 0.384, 0.187, 0.187, 0.243, 0.75, 0.25]
        # self.close()

    def clearAllText(self):
        # 遍历所有输入框，清空文本内容
        for input_widget in self.matrix_inputs:
            matrix = []
            for row_inputs in input_widget.input_fields:
                for all_input in row_inputs:
                    all_input.clear()
        self.result_label.setText("重置成功！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MatrixInputApp()
    window.show()
    sys.exit(app.exec_())
