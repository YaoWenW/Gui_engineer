import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, \
    QTableWidgetItem, QPushButton, QLineEdit, QLabel, QDialog,QScrollArea
from PyQt5.QtCore import Qt
import demo_main as demo

class ResultWindow(QDialog):
    def __init__(self, matrix, cols, parent=None):
        super().__init__(parent)
        self.setWindowTitle('确定度计算结果')
        # self.setGeometry(200, 100, 670, 600)
        self.resize(670, 500)
        layout = QVBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(cols))
        self.tableWidget.setColumnCount(5)

        # 设置表头标签
        horizontal_headers = ['一级', '二级', '三级', '四级', '五级']
        vertical_headers = [f'{cols[i]}' for i in range(len(cols))]

        self.tableWidget.setHorizontalHeaderLabels(horizontal_headers)
        self.tableWidget.setVerticalHeaderLabels(vertical_headers)

        # 显示计算结果在表格中
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                item = QTableWidgetItem('{:g}'.format(matrix[i][j]))
                self.tableWidget.setItem(i, j, item)

        layout.addWidget(self.tableWidget)

        close_button = QPushButton('保存并返回')
        close_button.clicked.connect(self.close)  # 关闭按钮的槽函数为关闭窗口
        layout.addWidget(close_button)

        self.setLayout(layout)

class MatrixCalculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.input_values = []
        self.matrix = []

    def initUI(self):
        self.setWindowTitle('单指标确定度计算')
        self.resize(400, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()

        # 创建左侧部分的输入框和计算按钮
        input_layout = QVBoxLayout()

        input_label = QLabel("请根据鼠标悬停提示信息或评价标准表，输入项目以下因素的取值:")
        input_layout.addWidget(input_label)

        scroll_area = QScrollArea()  # 创建QScrollArea用于放置输入框和标签
        scroll_widget = QWidget()  # 创建QWidget作为QScrollArea的子部件
        scroll_layout = QVBoxLayout(scroll_widget)  # 创建垂直布局用于放置输入框和标签

        self.input_lineedits = []
        self.cols = ['管片材料', '管片质量', '防水材料类型', '防水材料老化特性', '密封垫构型', '密封垫固定形式', '密封垫布置形式',
                     '纵缝接头刚度', '环缝抗剪刚度', '内部结构类型',
                     '水压', '不均匀地层', '温度影响', '水位影响',
                     '施工期上浮变形', '拼装精度', '姿态控制', '成型管片',
                     '水位影响', '纵向应力松弛']
        self.cols = ['管片材料', '管片质量', '防水材料类型', '防水材料老化特性', '密封垫构型', '密封垫固定形式', '密封垫布置形式',
                     '纵缝接头刚度', '环缝抗剪刚度', '内部结构类型',
                     '水压', '不均匀地层', '温度影响', '水位影响']

        self.info = [
                    '管片抗渗等级为P4时取[0, 20)，P6时取[20, 40)，P8时取[40, 60)，P10时取[60, 80)，P12时取[80, 100)',
                    '管片如果出现裂缝取[0, 20)，缺块掉角取[20, 40)，预埋部位缺陷取[40, 60)，出现气泡 / 蜂窝 / 麻面时取[60, 80)，完整无缺陷时取[80, 100)',
                    '材料类型如果为丁晴橡胶取[0, 20)，氯丁橡胶取[20, 40)，遇水膨胀橡胶取[40, 60)，三元乙丙橡胶取[60, 80)，遇水膨胀橡胶 + 三元乙丙橡胶取[80, 100)',
                    '按照管片材料的服役年限取值（以年为单位）',
                    '按照设防水压 / 设计水压取值',
                    '如果固定形式为粘贴式取[60, 80)，预埋 / 锚固式取[80, 100), 其余取值为[0, 60)',
                    '密封垫为遇水膨胀橡胶时取[0, 20)，单道密封垫取[20, 40)，双道 + 遇水膨胀橡胶取[40, 60)，双道同侧布置取[60, 80)，双道两侧布置取[80, 100)',

                    '纵缝螺栓数量为二斜取[0, 20)，三斜取[20, 40)，三斜交叉取[40, 60)，四斜取[60, 80)，四斜交叉取[80, 100)',
                    '环缝螺栓数量取值根据螺栓的实际数量取值。',
                    '内部结构类型为单层或双层时取[60, 80)，二次衬砌取[80, 100)，其余取值[0, 60]',

                    '取实际水压值（单位为Mpa）',
                    '取两个地层地基土基床系数比k1 / k2的值。',
                    '取温差值（单位为°C）',
                    '取水位差（单位为m）',
        ]
        for i in range(len(self.cols)):
            ls = {0: '材料因素', 7: '结构抗变形因素', 11: '水文地质条件因素', 14: '施工期影响因素', 18: '运营期影响因素'}
            if i in ls:
                input_layout_input1 = QHBoxLayout()
                # 创建标签
                label = QLabel(ls[i])
                # 设置标签字体样式
                label.setStyleSheet(" color: red;")
                input_layout_input1.addWidget(label)
                scroll_layout.addLayout(input_layout_input1)

            input_layout_input = QHBoxLayout()
            input_label = QLabel(f'{self.cols[i]}:')
            input_label.setToolTip(f"{self.info[i]}")
            input_label.setFixedWidth(120)  # 设置标签宽度
            input_edit = QLineEdit()
            input_edit.setFixedWidth(120)  # 设置输入框宽度
            input_edit.setAlignment(Qt.AlignLeft)  # 将输入框文本左对齐
            input_edit.setToolTip(f"{self.info[i]}")
            input_layout_input.addWidget(input_label)
            input_layout_input.addWidget(input_edit)
            scroll_layout.addLayout(input_layout_input)

            self.input_lineedits.append(input_edit)
        # Y = [100, 100, 100, 7, 2.8, 100, 100, 58, 30, 80, 0.72, 2.5, 6, 7.13, 11.46, 1.1, 7, 1.5, 7, 1]
        Y = [90, 90, 70, 0, 2.827, 70, 50, 30, 58, 70, 0.566, 2.5, 6, 8.68]

        for i in range(len(self.input_lineedits)):
            self.input_lineedits[i].setText(str(Y[i]))

        scroll_area.setWidget(scroll_widget)  # 将QWidget设置为QScrollArea的子部件
        scroll_area.setWidgetResizable(True)  # 设置QScrollArea可以调整大小
        input_layout.addWidget(scroll_area)

        calculate_button = QPushButton('计算')
        calculate_button.clicked.connect(self.showResultWindow)
        input_layout.addWidget(calculate_button)

        self.pushButton_clear = QPushButton('重置输入')
        self.pushButton_clear.clicked.connect(self.clearAllText)
        input_layout.addWidget(self.pushButton_clear)

        self.pushButton_fig = QPushButton('查看因素评价标准表')
        input_layout.addWidget(self.pushButton_fig)

        self.pushButton_save = QPushButton('保存结果并返回')
        input_layout.addWidget(self.pushButton_save)
        #
        layout.addLayout(input_layout)
        central_widget.setLayout(layout)

    def showResultWindow(self):
        # self.matrix = []
        if '' in [edit.text() for edit in self.input_lineedits]:
            return
        # 获取用户输入的值
        self.input_values = [float(edit.text()) for edit in self.input_lineedits]
        # 根据一定的公式计算矩阵
        self.matrix = demo.cal_N(self.input_values)
        result_window = ResultWindow(self.matrix, self.cols, self)
        result_window.exec_()
    def clearAllText(self):
        for edit in self.input_lineedits:
            edit.clear()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MatrixCalculator()
    window.show()
    sys.exit(app.exec_())
