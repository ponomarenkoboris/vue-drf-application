import { FormItemRule } from 'naive-ui'

export function personalInfoValidation(placeholder: string) {
    return (_: FormItemRule, value: string): boolean | Error => {
        if (value.trim().length === 0) {
            return new Error(`${placeholder} name cannot be empty`)
        }
        if (/\d/g.test(value)) {
            return new Error(`${placeholder} name cannot contain numbers`)
        }
        return true
    }
}

export function passwordValidation(_: FormItemRule, value: string): boolean | Error {
    if (value.trim().length === 0) return new Error('Password field cannot be empty!')
    if (!/\d/.test(value) && !/^(?![A-Z ,.'-]+$)(?![a-z ,.'-]+$)[a-zA-Z ,.'-]+$/.test(value)) {
        return new Error('Password must contain at least one number and one capital letter')
    }
    return true
}

export function usernameValidation(_: FormItemRule, value: string): boolean | Error {
    if (value.trim().length === 0) return new Error('Username cannot be empty!')
    return true
}

export function validatePasswordSame(profileObject: { password: string }) {
    return (_: FormItemRule, value: string): boolean | Error => {
        return value === profileObject.password ? true : new Error('Password is not same as re-entered password')
    }
}

const formRules = {
    username: {
        validator: usernameValidation,
        trigger: 'input',
    },
    firstName: {
        trigger: 'input',
        validator: personalInfoValidation('First')
    },
    lastName: {
        trigger: 'input',
        validator: personalInfoValidation('Last')
    },
    password: {
        trigger: 'input',
        validator: passwordValidation
    }
}

export default formRules