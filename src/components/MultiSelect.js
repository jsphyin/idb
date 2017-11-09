import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';

class MultiSelect extends React.Component {
    constructor(props) {
        super(props);
        this.displayName = props.name;
        this.state = {
            removeSelected: true,
            disabled: false,
            stayOpen: false,
            value: [],
            rtl: false
        };
    }

    handleSelectChange (value) {
        this.state.value = value;
        this.setState(this.state);
        console.log(this.state)
    }

    render () {
        var options = [];
        for(var i = 0; i < this.props.options.length; i++) {
            options.push({label: this.props.options[i].label, value: this.props.options[i].value.toString()});
        }
        return (
            <Select
                closeOnSelect={!this.state.stayOpen}
                disabled={false}
                multi
                joinValues
                delimiter=','
                onChange={this.handleSelectChange.bind(this)}
                options={options}
                placeholder={this.displayName}
                removeSelected={true}
                rtl={false}
                simpleValue
                value={this.state.value}
            />
        );
    }
}
MultiSelect.propTypes = {
    label: PropTypes.string
};

export default MultiSelect;
