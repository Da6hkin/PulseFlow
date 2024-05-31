module.exports = {
  "env": {
      "browser": true,
      "es2021": true
  },
  "extends": [
      "standard-with-typescript",
      "plugin:react/recommended"
  ],
  "overrides": [
      {
          "env": {
              "node": true
          },
          "files": [
              ".eslintrc.{js,cjs}"
          ],
          "parserOptions": {
              "sourceType": "script"
          }
      }
  ],
  "parserOptions": {
      "ecmaVersion": 12,
      "sourceType": "module",
      "project": "./tsconfig.json"
  },
  "plugins": [
      "react"
  ],
  "rules": {
      "@typescript-eslint/explicit-function-return-type": "off",
      "@typescript-eslint/strict-boolean-expressions": "off",
      "@typescript-eslint/no-unused-vars": ["warn"],
      "@typescript-eslint/no-confusing-void-expression": "off",
      "@typescript-eslint/promise-function-async": "off",
      "@typescript-eslint/no-dynamic-delete": "off",
      "@typescript-eslint/no-non-null-assertion": "off",
      "@typescript-eslint/no-misused-promises": "off",
      '@typescript-eslint/camelcase': 'off',
      "@typescript-eslint/restrict-plus-operands": [
          "error",
          {
              "checkCompoundAssignments": true
          }
      ],
      "react/display-name": "off"
  }
}