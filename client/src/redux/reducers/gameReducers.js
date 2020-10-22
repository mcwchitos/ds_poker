import constants from '../constants';

const initialState = [];


export const game = (state = initialState, action) => {
    switch (action.type) {
        case constants.game.GET_CARDS + constants.requestStatus.SUCCESS:
            return {
                ...state,
                cards: action.payload
            };
        case constants.game.EVALUATE_HANDS + constants.requestStatus.SUCCESS:
            return {
                ...state,
                isWInner:action.payload.isWinner,
                amounts: action.payload.amounts
            };
        case constants.game.CHANGE_CARDS + constants.requestStatus.SUCCESS:
            return {
                ...state,
                cards: action.payload
            };
        case constants.game.GET_AMOUNTS + constants.requestStatus.SUCCESS:
            return {
                ...state,
                amounts: action.payload
            };
        case constants.game.UPDATE_AMOUNT + constants.requestStatus.SUCCESS:
            return {
                ...state,
                amounts: action.payload.amounts,
                isTurn: false, 
                isEnd: action.payload.isEnd
            };
        case constants.game.GET_IS_TURN + constants.requestStatus.SUCCESS:
            return {
                ...state,
                isTurn: action.payload
            };
        case constants.game.GET_BETS + constants.requestStatus.SUCCESS:
            return {
                ...state,
                bets: action.payload
            };
        default:
            return state;
    }
};



