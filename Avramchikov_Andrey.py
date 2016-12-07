EMPLOYEES = {
    "First Name": 16,
    "Second Name": 31,
    "Third Name": 15,
    "Forth Name": 38,
    "Fifth Name": 25,
    "Sixth Name": 23
}

TASKS = {
    "First task": 3,
    "Second task": 4,
    "Third task": 7,
    "Forth task": 8,
    "Fifth task": 2,
    "Sixth task": 1,
    "Seventh task": 4,
    "Eighth task": 1,
    "Nineth task": 2,
    "Tenth task": 4,
    "Eleventh task": 4,
    "Twelfth task": 5
}


class Employee(object):
    def __init__(self, name, task_point):
        self.name = name
        self.task_point = task_point
        self.tasks = []
        self.tasks_count = 0
        self.tasks_point_sum = 0

    @property
    def capacity(self):
        return float(self.tasks_point_sum) / self.task_point * 100

    def append(self, task, max_allowed_sum=None):
        if max_allowed_sum is None:
            max_allowed_sum = self.task_point

        if (task.task_point + self.tasks_point_sum) > max_allowed_sum:
            return False
        else:
            self.tasks.append(task)
            self.tasks_count += 1
            self.tasks_point_sum += task.task_point
            return True


class Task(object):
    def __init__(self, name, task_point):
        self.name = name
        self.task_point = task_point


class TaskDispatcher(object):
    def __init__(self, employees):
        self.employees = employees
        self.tasks = []
        self.task_point_sum = 0
        self.employees_point_sum = 0
        self.capacity = 0

    def sort_employees(self, attr='task_point', reverse=True):
        self.employees.sort(key=lambda item: getattr(item, attr), reverse=reverse)

    def dispatch(self, tsks):
        self.tasks = tsks
        self.task_point_sum = sum(tsk.task_point for tsk in self.tasks)
        self.employees_point_sum = sum(employee.task_point for employee in self.employees)
        self.capacity = float(self.task_point_sum) / self.employees_point_sum
        if self.capacity > 1:
            raise ValueError('Please specify tasks with sum points less than possible for these employees')

        self.tasks.sort(key=lambda x: x.task_point, reverse=True)
        self.sort_employees()

        for task in self.tasks:
            add = False
            for emp in self.employees:
                max_allowed_sum = emp.task_point * self.capacity
                add = emp.append(task, max_allowed_sum)
                if add:
                    break

            if not add:
                self.sort_employees(attr='capacity', reverse=False)
                for emp in self.employees:
                    add = emp.append(task)
                    if add:
                        break


if __name__ == '__main__':
    employees = [Employee(name=key, task_point=value) for key, value in EMPLOYEES.iteritems()]
    tasks = [Task(name=key, task_point=value) for key, value in TASKS.iteritems()]

    task_dispatcher = TaskDispatcher(employees=employees)
    task_dispatcher.dispatch(tasks)

    for employee in task_dispatcher.employees:
        print '{}-Task Point: {}; Task point sum: {};  Capacity: {}%'.format(employee.name, employee.task_point,
                                                                             employee.tasks_point_sum,
                                                                             employee.tasks_point_sum * 100 / employee.task_point)
        for task in employee.tasks:
            print '[{}]: {}'.format(task.name, task.task_point)
