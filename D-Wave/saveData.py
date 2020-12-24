from datetime import datetime
import csv


def save_data(P, Computer_Name, circuit_Size, gap_size, graph_size, output):
    now = datetime.now()
    name = "n" + str(P) + "c" + Computer_Name + "circuit" + str(circuit_Size) + "time" + str(now) + "gap" + str(
        gap_size) + "graph" + str(graph_size) + '.csv'
    length = len(output['Results'])
    index = ['a', 'b', 'valid', 'Percentage_of_results']
    with open(name, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        time = ['Time', output['Timing']['Actual']['QPU processing time']]
        csv_writer.writerow(time)
        csv_writer.writerow(index)
        for i in range(length):
            data = [output['Results'][i]['a'], output['Results'][i]['b'], output['Results'][i]['Valid'],
                    output['Results'][i]['Percentage of results']]
            csv_writer.writerow(data)
