import tkinter as tk

class FormBuilder:
    def __init__(self, parent):
        self.parent = parent
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)
        return field
    
    def text(self, key, label, default="", required=False):
        return self.add_field(TextField(key, label, default, required))
    
    def toggle(self, key, label, default=False, required=False):
        return self.add_field(ToggleField(key, label, default, required))
    
    def multi_button(self, key, label, options, default=None, required=False):
        return self.add_field(MultiButtonField(key, label, options, default, required))
    
    def render(self):
        for row, field in enumerate(self.fields):
            field.render(self.parent, row)
        self.parent.grid_columnconfigure(1, weight=1)

    def validate(self):
        errors = []
        for field in self.fields:
            error = field.validate()
            if error:
                errors.append(error)
        return errors

    def get_export_data(self):
        return {field.key: field.get_value() for field in self.fields}


class BaseField:
    def __init__(self, key, label, default=None, required=False):
        self.key = key
        self.label = label
        self.default = default
        self.required = required

    def render(self, parent, row):
        raise NotImplementedError("Subclasses must implement render()")
        
    def get_value(self):
        raise NotImplementedError("Subclasses must implement get_value()")
    
    def validate(self):
        value = self.get_value()
        if self.required:
            if value is None:
                return f"{self.label} is required."
            if isinstance(value, str) and not value.strip():
                return f"{self.label} cannot be empty."
            if isinstance(value, list) and len(value) == 0:
                return f"{self.label} must have at least one selection."
        return None
        

class TextField(BaseField):
    def __init__(self, key, label, default="", required=False):
        super().__init__(key, label, default, required)
        self.var = tk.StringVar(value=default)
        self.entry = None

    def render(self, parent, row):
        tk.Label(parent, text=self.label).grid(row=row, column=0, sticky="w", padx=5, pady=5)
        self.entry = tk.Entry(parent, textvariable=self.var)
        self.entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)

    def get_value(self):
        return self.var.get()


class ToggleField(BaseField):
    def __init__(self, key, label, default=False, required=False):
        super().__init__(key, label, default, required)
        self.var = tk.BooleanVar(value=default)

    def render(self, parent, row):
        tk.Label(parent, text=self.label).grid(row=row, column=0, sticky="w", padx=5, pady=5)
        tk.Checkbutton(parent, variable=self.var).grid(row=row, column=1, sticky="w", padx=5, pady=5)

    def get_value(self):
        return self.var.get()


class MultiButtonField(BaseField):
    def __init__(self, key, label, options, default=None, required=False):
        super().__init__(key, label, default if default is not None else options[0], required)
        self.options = options
        self.var = tk.StringVar(value=self.default)

    def render(self, parent, row):
        tk.Label(parent, text=self.label).grid(row=row, column=0, sticky="nw", padx=5, pady=5)
        
        button_frame = tk.Frame(parent)
        button_frame.grid(row=row, column=1, sticky="w", padx=5, pady=5)

        for i, option in enumerate(self.options):
            tk.Radiobutton(
                button_frame,
                text=option,
                variable=self.var,
                value=option,
                indicatoron=0,
                width=12
            ).grid(row=0, column=i, padx=2, pady=2)

    def get_value(self):
        return self.var.get()