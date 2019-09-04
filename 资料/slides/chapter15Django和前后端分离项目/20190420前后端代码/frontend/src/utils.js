import React from 'react';
const inject =  obj=>  Comp => props => <Comp {...props} {...obj} />;

/**
 * 
 * @param {*} qs 查询字符串
 * @param {*} re 正则表达式
 */
function parse_qs(qs, re=/(\w+)=([^&=]+)/) {
    if (qs.startsWith('?'))
    qs = qs.substr(1);
    let obj = {}
    qs.split('&').forEach(x => {
        let m = re.exec(x)
        if (m) {
            obj[m[1]] = m[2]
        }
    });
    return obj
}

export {inject, parse_qs};


