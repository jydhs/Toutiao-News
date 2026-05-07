import { computed, defineComponent, createVNode as _createVNode } from "vue";
import { addUnit, truthProp, numericProp, createNamespace } from "../utils/index.mjs";
const [name, bem] = createNamespace("progress");
const progressProps = {
  color: String,
  inactive: Boolean,
  pivotText: String,
  textColor: String,
  showPivot: truthProp,
  pivotColor: String,
  trackColor: String,
  strokeWidth: numericProp,
  percentage: {
    type: numericProp,
    default: 0,
    validator: (value) => +value >= 0 && +value <= 100
  }
};
var stdin_default = defineComponent({
  name,
  props: progressProps,
  setup(props, {
    slots
  }) {
    const background = computed(() => props.inactive ? void 0 : props.color);
    const format = (rate) => Math.min(Math.max(+rate, 0), 100);
    const renderPivot = () => {
      const {
        textColor,
        pivotText,
        pivotColor,
        percentage
      } = props;
      const safePercentage = format(percentage);
      const text = pivotText != null ? pivotText : `${safePercentage}%`;
      if (props.showPivot && (slots.pivot || text)) {
        const style = {
          color: textColor,
          left: `${safePercentage}%`,
          transform: `translate(-${safePercentage}%,-50%)`,
          background: pivotColor || background.value
        };
        return _createVNode("span", {
          "style": style,
          "class": bem("pivot", {
            inactive: props.inactive
          })
        }, [slots.pivot ? slots.pivot({
          percentage: safePercentage
        }) : text]);
      }
    };
    return () => {
      const {
        trackColor,
        percentage,
        strokeWidth
      } = props;
      const safePercentage = format(percentage);
      const rootStyle = {
        background: trackColor,
        height: addUnit(strokeWidth)
      };
      const portionStyle = {
        width: `${safePercentage}%`,
        background: background.value
      };
      return _createVNode("div", {
        "class": bem(),
        "style": rootStyle
      }, [_createVNode("span", {
        "class": bem("portion", {
          inactive: props.inactive
        }),
        "style": portionStyle
      }, null), renderPivot()]);
    };
  }
});
export {
  stdin_default as default,
  progressProps
};
