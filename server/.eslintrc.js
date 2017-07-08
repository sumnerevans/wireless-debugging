module.exports = {
  env: {
    browser: true,
    es6: true,
    jquery: true,
    mocha: true,
    node: true,
  },

  plugins: [
    'requirejs',
  ],

  parserOptions: {
    ecmaVersion: 6,
    sourceType: 'module',
    ecmaFeatures: {
      arrowFunctions: true,
      binaryLiterals: true,
      blockBindings: true,
      classes: true,
      defaultParams: true,
      destructuring: true,
      forOf: true,
      generators: true,
      modules: true,
      objectLiteralComputedProperties: true,
      objectLiteralDuplicateProperties: true,
      objectLiteralShorthandMethods: true,
      objectLiteralShorthandProperties: true,
      octalLiterals: true,
      regexUFlag: true,
      regexYFlag: true,
      spread: true,
      superInFunctions: true,
      templateStrings: true,
      unicodeCodePointEscapes: true,
      globalReturn: true,
      jsx: true,
    },
  },

  // Use the suggested ESLint settings as a base
  extends: [
    'eslint:recommended',
    'plugin:requirejs/recommended',
  ],

  rules: {
    //
    // Possible Errors
    // These rules relate to possible syntax or logic errors in JavaScript code
    //
    'for-direction': 2,
    'no-extra-parens': [2, 'all', { nestedBinaryExpressions: false }],
    'no-template-curly-in-string': 1,
    'valid-jsdoc': 2,

    //
    // Best Practices
    //
    // These rules relate to better ways of doing things to help you avoid
    // problems.
    //
    'array-callback-return': 2,
    'block-scoped-var': 2,
    'class-methods-use-this': 1,
    'consistent-return': 2,
    curly: 2,
    'default-case': 1,
    'dot-location': [2, 'property'],
    'dot-notation': 2,
    eqeqeq: 2,
    'guard-for-in': 2,
    'no-alert': 2,
    'no-caller': 2,
    'no-div-regex': 2,
    'no-else-return': 1,
    'no-empty-function': 1,
    'no-eq-null': 2,
    'no-eval': 2,
    'no-extra-bind': 2,
    'no-floating-decimal': 2,
    'no-implicit-coercion': 2,
    'no-implicit-globals': 2,
    'no-implied-eval': 2,
    'no-invalid-this': 2,
    'no-iterator': 2,
    'no-labels': 2,
    'no-lone-blocks': 2,
    'no-loop-func': 2,
    'no-multi-spaces': [2, { ignoreEOLComments: false }],
    'no-multi-str': 2,
    'no-new': 2,
    'no-new-func': 2,
    'no-new-wrappers': 2,
    'no-octal-escape': 2,
    'no-proto': 2,
    'no-return-assign': 2,
    'no-return-await': 2,
    'no-script-url': 2,
    'no-self-compare': 2,
    'no-sequences': 2,
    'no-throw-literal': 2,
    'no-unmodified-loop-condition': 2,
    'no-unused-expressions': 2,
    'no-useless-call': 2,
    'no-useless-concat': 2,
    'no-useless-return': 2,
    'no-void': 2,
    'no-warning-comments': [1, {
      terms: ['todo', 'fixme', 'xxx', 'hack', 'debug'],
      location: 'start',
    }],
    'no-with': 2,
    'prefer-promise-reject-errors': 2,
    radix: 2,
    'require-await': 2,
    'vars-on-top': 1,
    'wrap-iife': [2, 'inside'],
    yoda: 1, // Require or disallow Yoda conditions

    //
    // Strict Mode
    //
    // These rules relate to using strict mode.
    //
    strict: [2, 'safe'],

    //
    // Variables
    //
    // These rules have to do with variable declarations.
    //
    'no-catch-shadow': 2,
    'no-delete-var': 2,
    'no-label-var': 2,
    'no-shadow': 2,
    'no-shadow-restricted-names': 2,
    'no-undef-init': 2,
    'no-undefined': 2,
    'no-use-before-define': 2,

    //
    // Node.js and CommonJS
    //
    // These rules relate to code running in Node.js, or in browsers with
    // CommonJS.
    'callback-return': 2,
    'global-require': 2,
    'handle-callback-err': 1,
    'no-buffer-constructor': 2,
    'no-mixed-requires': 2,
    'no-path-concat': 2,
    'no-process-env': 2,

    //
    // Stylistic Issues
    //
    // These rules are purely matters of style and are quite subjective.
    //
    'array-bracket-spacing': [2, 'never'],
    'block-spacing': [2, 'always'],
    'brace-style': 2,
    camelcase: 1,
    'capitalized-comments': [2, 'always', { ignoreConsecutiveComments: true }],
    'comma-dangle': [2, 'always-multiline'],
    'comma-spacing': [2, {
      before: false,
      after: true,
    }],
    'comma-style': [2, 'last'],
    'computed-property-spacing': 2,
    'eol-last': 2,
    'func-call-spacing': 2,
    indent: [2, 2, {
      SwitchCase: 1,
      VariableDeclarator: { var: 2, let: 2, const: 3 },
      FunctionDeclaration: { parameters: 'first', body: 1 },
      FunctionExpression: { parameters: 'first', body: 1 },
      CallExpression: { arguments: 1 },
      ArrayExpression: 1,
      ObjectExpression: 1,
    }],
    'jsx-quotes': [2, 'prefer-double'],
    'key-spacing': 2,
    'keyword-spacing': 2,
    'linebreak-style': 2,
    'max-len': [2, {
      ignoreUrls: true,
      ignoreStrings: true,
      ignoreTemplateLiterals: true,
    }],
    'max-nested-callbacks': 1,
    'max-statements-per-line': 2,
    'new-cap': 2,
    'new-parens': 2,
    'no-array-constructor': 1,
    'no-bitwise': 1,
    'no-lonely-if': 1,
    'no-mixed-operators': 2,
    'no-multi-assign': 2,
    'no-multiple-empty-lines': 2,
    'no-nested-ternary': 1,
    'no-new-object': 2,
    'no-plusplus': 0,
    'no-tabs': 2,
    'no-trailing-spaces': 2,
    'no-unneeded-ternary': 1,
    'no-whitespace-before-property': 2,
    'object-curly-newline': [2, { consistent: true }],
    'object-curly-spacing': [2, 'always'],
    'one-var': [2, 'never'],
    'one-var-declaration-per-line': [2, 'always'],
    'operator-linebreak': [2, 'after'],
    'padded-blocks': [2, 'never'],
    'quote-props': [1, 'as-needed'],
    quotes: [1, 'single'],
    'require-jsdoc': [1, {
      require: {
        FunctionDeclaration: true,
        MethodDefinition: true,
        ClassDeclaration: true,
        ArrowFunctionExpression: false,
      },
    }],
    semi: [2, 'always'],
    'semi-style': [2, 'last'],
    'space-before-blocks': [2, 'always'],
    'space-before-function-paren': [2, {
      anonymous: 'never',
      named: 'never',
      asyncArrow: 'always',
    }],
    'space-in-parens': [2, 'never'],
    'space-infix-ops': 2,
    'space-unary-ops': [2, {
      words: true,
      nonwords: false,
    }],
    'spaced-comment': [2, 'always', {
      block: { balanced: true },
    }],
    'switch-colon-spacing': 2,
    'wrap-regex': 2,

    //
    // ECMAScript 6
    //
    // These rules relate to ES6, also known as ES2015.
    //
    'arrow-body-style': [2, 'as-needed', {
      requireReturnForObjectLiteral: true,
    }],
    'arrow-parens': [2, 'as-needed'],
    'arrow-spacing': 2,
    'generator-star-spacing': [2, {
      before: false,
      after: false,
    }],
    'no-duplicate-imports': 2,
    'no-new-symbol': 2,
    'no-useless-computed-key': 2,
    'no-useless-constructor': 2,
    'no-useless-rename': 2,
    'no-var': 2,
    'prefer-arrow-callback': 2,
    'prefer-const': 2,
    'prefer-numeric-literals': 2,
    'prefer-rest-params': 2,
    'prefer-spread': 2,
    'prefer-template': 2,
    'rest-spread-spacing': 2,
    'symbol-description': 1,
    'template-curly-spacing': 2,
    'yield-star-spacing': 2,
  },

  globals: {},
};
