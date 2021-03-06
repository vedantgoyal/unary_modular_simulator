class Connector:
    # Connectors are inputs and outputs. Only outputs should connect
    # to inputs. Be careful NOT to have circular references
    # As an output is changed it propagates the change to its connected inputs
    
    def __init__(self, owner, name, activates=0, monitor=0):
        self.value = None
        self.owner = owner
        self.name = name
        self.monitor = monitor
        self.connects = []
        self.activates = activates   # If true change kicks evaluate function

    def connect(self, inputs):
        if not isinstance(inputs, list):
            inputs = [inputs]
        for input in inputs:
            self.connects.append(input)

    def set(self, value):
        if self.value == value:
            return      # Ignore if no change
        self.value = value
        #if self.name == "Clk":
        #    self.owner.evaluate_clk()
        if self.activates:
            self.owner.evaluate()
        if self.monitor:
            print("Connector {0}-{1} set to {2}".format(self.owner.name,
                                                        self.name,
                                                        self.value))
        for con in self.connects:
            con.set(value)
