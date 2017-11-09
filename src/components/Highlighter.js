import { findAll } from 'highlight-words-core'
import PropTypes from 'prop-types'
import React from 'react'

Highlighter.propTypes = {
    activeClassName: PropTypes.string,
    activeIndex: PropTypes.number,
    activeStyle: PropTypes.object,
    autoEscape: PropTypes.bool,
    className: PropTypes.string,
    highlightClassName: PropTypes.string,
    highlightStyle: PropTypes.object,
    highlightTag: PropTypes.oneOfType([
        PropTypes.node,
        PropTypes.func,
        PropTypes.string
    ]),
    sanitize: PropTypes.func,
    searchWords: PropTypes.arrayOf(PropTypes.string).isRequired,
    textToHighlight: PropTypes.string.isRequired,
    unhighlightClassName: PropTypes.string,
    unhighlightStyle: PropTypes.object
}

/**
 * Highlights all occurrences of search terms (searchText) within a string (textToHighlight).
 * This function returns an array of strings and <span>s (wrapping highlighted words).
 */
export default function Highlighter ({
    activeClassName = '',
    activeIndex = -1,
    activeStyle,
    autoEscape,
    caseSensitive = false,
    className,
    highlightClassName = '',
    highlightStyle = {},
    highlightTag = 'mark',
    sanitize,
    searchWords,
    textToHighlight,
    unhighlightClassName = '',
    unhighlightStyle
}) {
    const chunks = findAll({
        autoEscape,
        caseSensitive,
        sanitize,
        searchWords,
        textToHighlight
    })
    const HighlightTag = highlightTag
    let highlightCount = -1
    let highlightClassNames = ''
    let highlightStyles

    return (
        <span className={className}>
        {chunks.map((chunk, index) => {
            const text = textToHighlight.substr(chunk.start, chunk.end - chunk.start)

            if (chunk.highlight) {
                highlightCount++

                const isActive = highlightCount === +activeIndex

                highlightClassNames = `${highlightClassName} ${isActive ? activeClassName : ''}`
                highlightStyles = isActive === true && activeStyle != null
                    ? Object.assign({}, highlightStyle, activeStyle)
                    : highlightStyle

                return (
                    <HighlightTag
                    className={highlightClassNames}
                    key={index}
                    style={highlightStyles}
                    >
                    {text}
                    </HighlightTag>
                )
            } else {
                return (
                    <span
                    className={unhighlightClassName}
                    key={index}
                    style={unhighlightStyle}
                    >
                    {text}
                    </span>
                )
            }
        })}
        </span>
    )
}
