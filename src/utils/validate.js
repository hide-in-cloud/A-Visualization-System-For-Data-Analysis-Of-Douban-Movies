/**
 * Created by TanShaoKuang on 2023/2/28.
 */

/**
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validUsername(str) {
  return !/^(?![0-9]*$)(?![a-zA-Z]*$)[a-zA-Z0-9]{4,16}$/.test(str)
}
