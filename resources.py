import csv

def key_check(Dictionary, string):
    try:
        output = Dictionary[string]
    except KeyError:
        output = "BLANK"
    return output


def variable_write(values, Name):
    # if values['Member Type'] == 'Beam':
    with open(Name + '.txt', 'w', newline='') as csv_file:
        data = [[str(i), values[i]] for i in values]
        print(data)
        writer = csv.writer(csv_file)
        writer.writerows(data)

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def variable(Name):
    Dictionary = {}
    with open(str(Name) + '.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            Dictionary[row[0]] = row[1]
    return Dictionary


def blank(n):
    layout = [[]]
    for i in range(n):
        layout += [[Sg.Text('')]]
    return layout

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg