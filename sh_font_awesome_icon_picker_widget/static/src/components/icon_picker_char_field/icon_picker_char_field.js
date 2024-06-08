/** @odoo-module **/
import { _lt } from "@web/core/l10n/translation";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { formatChar } from '@web/views/fields/formatters';
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useDynamicPlaceholder } from "@web/views/fields/dynamicplaceholder_hook";
import { useInputField } from "@web/views/fields/input_field_hook";
import { Component, useExternalListener, useEffect, useRef,useState } from "@odoo/owl";
import { usePopover } from "@web/core/popover/popover_hook";
import { localization } from "@web/core/l10n/localization";
import { IconPickerPopover } from "@sh_font_awesome_icon_picker_widget/components/icon_picker_popover/IconPickerPopover";

export class IconPickerCharField extends Component {

    static template = "sh_font_awesome_icon_picker_widget.IconPickerCharField";

    static props = {
        ...standardFieldProps,
        hidden: { type: Boolean, optional: true },
        placeholder: { type: String, optional: true },
        dynamicPlaceholder: { type: Boolean, optional: true },
    };

    static defaultProps = { dynamicPlaceholder: false, hidden: true };

    setup() {
        super.setup();
        this.input = useRef("input");
        this.state = useState(
            {
                searchTerm: "",
                currentIcon: this.formattedValue
            }
        )        
        this.popover = usePopover();

        if (this.props.dynamicPlaceholder) {
            const dynamicPlaceholder = useDynamicPlaceholder(this.input);
            useExternalListener(document, "keydown", dynamicPlaceholder.onKeydown);
            useEffect(() =>
                dynamicPlaceholder.updateModel(this.props.dynamicPlaceholderModelReferenceField)
            );
        }

        useInputField({
            getValue: () => this.props.record.data[this.props.name] || "",
            parse: (v) => this.parse(v),
        });
    }

    closePopover() {
        this.popoverCloseFn();
        this.popoverCloseFn = null;
    }

    onClickOpenIconPicker(ev) {

        this.popoverCloseFn = this.popover.add(
            ev.target,
            IconPickerPopover,
            {
                onClose: this.closePopover,
                onSelect: this.onSelect.bind(this),
                state: this.state,
            },
            {
                position: localization.direction === "rtl" ? "bottom" : "left",
            },
        );
    }

    get formattedValue() {
        return formatChar(this.props.record.data[this.props.name]);
    }
    onSelect(value) {
        this.state.currentIcon = formatChar(value);
        this.props.record.update({ [this.props.name]: value });
        this.closePopover();
    }
}

IconPickerCharField.template = "sh_font_awesome_icon_picker_widget.IconPickerCharField";
IconPickerCharField.components = { IconPickerCharField };

IconPickerCharField.extractProps =({ attrs, options }) => ({
    dynamicPlaceholder: attrs.options.dynamic_placeholder,
    placeholder: attrs.placeholder,
});
IconPickerCharField.supportedTypes = ["char"];
IconPickerCharField.displayName = _lt("Icon Selection");

registry.category("fields").add("sh_fa_icon_picker_char", IconPickerCharField);

