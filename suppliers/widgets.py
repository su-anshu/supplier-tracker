# suppliers/widgets.py
from django import forms
from django.utils.safestring import mark_safe

class TransferWidget(forms.Widget):
    """
    Custom widget for transferring items between two lists
    """
    template_name = 'widgets/transfer_widget.html'
    
    def __init__(self, choices=(), attrs=None):
        super().__init__(attrs)
        self.choices = choices
    
    def format_value(self, value):
        if value is None:
            return []
        return [str(v) for v in value]
    
    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        
        selected_values = self.format_value(value)
        available_choices = []
        selected_choices = []
        
        for choice_value, choice_label in self.choices:
            choice_value = str(choice_value)
            if choice_value in selected_values:
                selected_choices.append((choice_value, choice_label))
            else:
                available_choices.append((choice_value, choice_label))
        
        widget_id = attrs.get('id', name)
        
        html = f'''
        <div class="transfer-widget" id="{widget_id}_widget">
            <div class="row">
                <div class="col-md-5">
                    <label class="form-label">Available:</label>
                    <select class="form-select available-list" size="8" multiple id="{widget_id}_available">
        '''
        
        for choice_value, choice_label in available_choices:
            html += f'<option value="{choice_value}">{choice_label}</option>'
        
        html += f'''
                    </select>
                </div>
                <div class="col-md-2 d-flex flex-column justify-content-center">
                    <button type="button" class="btn btn-primary btn-sm mb-2 transfer-btn" 
                            onclick="transferItems('{widget_id}_available', '{widget_id}_selected')">
                        <i class="fas fa-arrow-right"></i> Add
                    </button>
                    <button type="button" class="btn btn-secondary btn-sm" 
                            onclick="transferItems('{widget_id}_selected', '{widget_id}_available')">
                        <i class="fas fa-arrow-left"></i> Remove
                    </button>
                </div>
                <div class="col-md-5">
                    <label class="form-label">Selected:</label>
                    <select class="form-select selected-list" size="8" multiple id="{widget_id}_selected">
        '''
        
        for choice_value, choice_label in selected_choices:
            html += f'<option value="{choice_value}">{choice_label}</option>'
        
        html += f'''
                    </select>
                </div>
            </div>
            <input type="hidden" name="{name}" id="{widget_id}_hidden" value="{','.join(selected_values)}">
        </div>
        
        <script>
        function transferItems(fromId, toId) {{
            const fromSelect = document.getElementById(fromId);
            const toSelect = document.getElementById(toId);
            
            // Get the widget ID from the fromId or toId
            let widgetId = '';
            if (fromId.includes('available')) {{
                widgetId = fromId.replace('_available', '');
            }} else if (fromId.includes('selected')) {{
                widgetId = fromId.replace('_selected', '');
            }} else if (toId.includes('available')) {{
                widgetId = toId.replace('_available', '');
            }} else if (toId.includes('selected')) {{
                widgetId = toId.replace('_selected', '');
            }}
            
            const hiddenInput = document.getElementById(widgetId + '_hidden');
            
            if (!fromSelect || !toSelect || !hiddenInput) {{
                console.error('Transfer widget elements not found:', {{
                    fromSelect: !!fromSelect,
                    toSelect: !!toSelect, 
                    hiddenInput: !!hiddenInput,
                    widgetId: widgetId
                }});
                return;
            }}
            
            const selectedOptions = Array.from(fromSelect.selectedOptions);
            if (selectedOptions.length === 0) {{
                return; // No items selected
            }}
            
            // Move selected options
            selectedOptions.forEach(option => {{
                toSelect.appendChild(option);
                option.selected = false; // Deselect after moving
            }});
            
            // Update hidden field with all selected values from the "selected" listbox
            const selectedList = document.getElementById(widgetId + '_selected');
            if (selectedList) {{
                const values = Array.from(selectedList.options).map(option => option.value);
                hiddenInput.value = values.join(',');
                console.log('Updated hidden field:', hiddenInput.name, '=', hiddenInput.value);
            }}
        }}
        
        // Initialize hidden field on page load
        document.addEventListener('DOMContentLoaded', function() {{
            const selectedList = document.getElementById('{widget_id}_selected');
            const hiddenInput = document.getElementById('{widget_id}_hidden');
            if (selectedList && hiddenInput) {{
                const values = Array.from(selectedList.options).map(option => option.value);
                hiddenInput.value = values.join(',');
            }}
        }});
        </script>
        '''
        
        return mark_safe(html)
    
    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if value:
            return value.split(',')
        return []
