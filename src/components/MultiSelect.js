import React from 'react';
import PropTypes from 'prop-types';
import VirtualizedSelect from 'react-virtualized-select';

class MultiSelect extends React.Component {
    constructor(props) {
        super(props);
        this.displayName = props.name;
        this.state = {
            removeSelected: true,
            disabled: false,
            stayOpen: false,
            rtl: false
        };
    }

    handleSelectChange (values) {
        this.props.set_values(values);
    }

    render () {
        return (
            <VirtualizedSelect
                closeOnSelect={!this.state.stayOpen}
                disabled={false}
                multi
                joinValues
                delimiter='|'
                onChange={this.handleSelectChange.bind(this)}
                options={this.props.options}
                placeholder={this.displayName}
                removeSelected={true}
                rtl={false}
                simpleValue
                value={this.props.values}
            />
        );
    }
}
MultiSelect.propTypes = {
    label: PropTypes.string
};

export default MultiSelect;
