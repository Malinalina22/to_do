from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QGroupBox

app = QApplication([])

main_win = QWidget()
main_win.setWindowTitle('Планы')
main_win.resize(500, 400)

main_header = QLabel('Заметки')
add_button = QPushButton('Добавить')
delete_button = QPushButton('Удалить')
edit_button = QPushButton('Редактировать')
task_group = QGroupBox()
vbox = QVBoxLayout()
task_group.setLayout(vbox)

vlane = QVBoxLayout()
vlane.addWidget(main_header, alignment=Qt.AlignCenter)

hline = QHBoxLayout()
hline.addWidget(add_button)
hline.addWidget(delete_button)

vlane.addLayout(hline)
vlane.addWidget(task_group)
main_win.setLayout(vlane)

tasks = list()

def load_tasks():
    settings = QSettings("MyApp", "MyPlanApp")
    tasks_text = settings.value("tasks", type=str)
    if tasks_text:
        task_names = tasks_text.split()
        for task_name in task_names:
            task = QCheckBox(task_name)
            vbox.addWidget(task, alignment=Qt.AlignLeft)
            tasks.append(task)

def save_tasks():
    settings = QSettings("MyApp", "MyPlanApp")
    tasks_text = ' '.join([t.text() for t in tasks])
    settings.setValue("tasks", tasks_text)

def add_task():
    task_name, ok = QInputDialog.getText(main_win, 'Добавление новой задачи:', 'Введите задачу:')
    if ok and task_name != '':
        task = QCheckBox(task_name)
        vbox.addWidget(task, alignment=Qt.AlignLeft)
        tasks.append(task)
        save_tasks()

def delete_task():
    for task in tasks.copy():
        if task.isChecked():
            tasks.remove(task)
            task.setParent(None)
            save_tasks()

add_button.clicked.connect(add_task)
delete_button.clicked.connect(delete_task)

# Загрузка задач при запуске программы
load_tasks()

main_win.show()
app.exec_()

# Сохранение задач при закрытии программы
save_tasks()
