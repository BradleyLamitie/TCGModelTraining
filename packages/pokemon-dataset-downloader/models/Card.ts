import { InferSchemaType, model, Schema, Types } from "mongoose";

interface IAttack {
    damage : String,
    cost : String[],
    name : String,
    text : String,
    convertedEnergyCost : Number
} 

interface ILegality {
    unlimited : String
}

interface IPrice {
    avg30: Number,
    avg1: Number,
    reverseHoloLow: Number,
    averageSellPrice: Number,
    reverseHoloTrend: Number,
    reverseHoloAvg7: Number,
    lowPrice: Number,
    avg7: Number,
    reverseHoloAvg30: Number,
    lowPriceExPlus: Number,
    trendPrice: Number,
    reverseHoloAvg1: Number,
}

interface ICardMarket {
    prices : IPrice[],
    url : String,
    updatedAt : String
}

const attackSchema = new Schema({
    damage: { type: String },
    cost: { type: [String] },
    name: { type: String },
    text: { type: String },
    convertedEnergyCost: { type: Number },
}, { timestamps: true, _id: false  });

const legalitiesSchema = new Schema({
    unlimited: { type: String },
}, { timestamps: true, _id: false  });

const pricesSchema = new Schema({
    avg30: { type: Number },
    avg1: { type: Number },
    reverseHoloLow: { type: Number },
    averageSellPrice: { type: Number },
    reverseHoloTrend: { type: Number },
    reverseHoloAvg7: { type: Number },
    lowPrice: { type: Number },
    avg7: { type: Number },
    reverseHoloAvg30: { type: Number },
    lowPriceExPlus: { type: Number },
    trendPrice: { type: Number },
    reverseHoloAvg1: { type: Number },
}, { timestamps: true, _id: false  });

const cardmarketSchema = new Schema({
    prices: { type: pricesSchema },
    url: { type: String },
    updatedAt: { type: String }
}, { timestamps: true, _id: false  });

interface IImage {
    small : String,
    large : String
}

const imagesSchema = new Schema({
    small: { type: String },
    large: { type: String },
},{ timestamps: true, _id: false  });

interface IResistance {
    type : String, 
    value : String
}

const resistanceSchema = new Schema({
    type: { type: String },
    value: { type: String },
},{ timestamps: true, _id: false  });

interface ITCGPrice {
    market : Number,
    high : Number,
    low : Number,
    mid : Number
}

const tcgPriceSchema = new Schema({
    market: { type: Number },
    high: { type: Number },
    low: { type: Number },
    mid: { type: Number },
},{ timestamps: true, _id: false  })

interface ITCGPrices {
    holofoil : ITCGPrice,
    reverseHolofoil : ITCGPrice
}

const tcgPricesSchema = new Schema({
    holofoil: { type: tcgPriceSchema },
    reverseHolofoil: { type: tcgPriceSchema },
}, { timestamps: true, _id: false  })

interface ITCGPlayer {
    prices : ITCGPrices,
    url : String,
    updatedAt : String
}

const tcgPlayerSchema = new Schema({
    prices: { type: tcgPricesSchema },
    url: { type: String },
    updatedAt: { type: String }
}, { timestamps: true, _id: false  });

interface ISetImage {
    symbol : String,
    logo : String
}

const setImageSchema = new Schema({
    symbol: { type: String },
    logo: { type: String },
}, { timestamps: true, _id: false  })

interface ISet {
    total : Number,
    images : ISetImage,
    printedTotal : Number,
    ptcgoCode: String,
    releaseDate : String,
    series : String,
    name : String,
    legalities : ILegality[],
    id : String,
    updatedAt : String
}

const setSchema = new Schema({
    total: { type: Number, required: true },
    images: { type: [setImageSchema] },
    printedTotal: { type: Number},
    ptcgoCode: { type: String },
    releaseDate: { type: String },
    series: { type: String },
    name: { type: String },
    legalities: { type: [legalitiesSchema] },
    id: { type: String },
    updatedAt: { type: String },
}, { timestamps: true, _id: false });
 
interface ICardInfo {
    id: String ,
    artist: String ,
    attacks: [IAttack] ,
    cardmarket: [ICardMarket] ,
    convertedRetreatCost: Number ,
    hp: Number ,
    images: IImage ,
    legalities: ILegality ,
    level: String ,
    name: String ,
    nationalPokedexNumbers: [Number] ,
    number: String ,
    rarity: String ,
    resistances: [IResistance] ,
    retreatCost: [String] ,
    set: Types.ObjectId, required: true,
    setName: String,
    setTotalCards: Number,
    subtypes: [String] ,
    supertype: String ,
    tcgplayer: ITCGPlayer ,
    types: [String] ,
    weaknesses: [IResistance] 
}

const cardInfoSchema = new Schema({
    id: { type: String },
    artist: { type: String, default: "No Artist" },
    attacks: { type: [attackSchema] },
    cardmarket: { type: [cardmarketSchema] },
    convertedRetreatCost: { type: Number },
    hp: { type: Number },
    images: { type: imagesSchema },
    legalities: { type: legalitiesSchema },
    level: { type: String },
    name: { type: String },
    nationalPokedexNumbers: { type: [Number] },
    number: { type: String },
    rarity: { type: String },
    resistances: { type: [resistanceSchema] },
    retreatCost: { type: [String] },
    set: { type: setSchema, required: true },
    subtypes: { type: [String] },
    supertype: { type: String },
    tcgplayer: { type: tcgPlayerSchema },
    types: { type: [String] },
    weaknesses: { type: [resistanceSchema] }
}, { timestamps: true, _id: false  });

interface IAdditionalTag {
    tagName: String,
    tagValues: [String]
}

const additionalTagSchema = new Schema({
    tagName: String,
    tagValues: [String]
}, { timestamps: true, _id: false  });

export interface ICard {
    _id : Types.ObjectId,
    cardInfo : ICardInfo,
    lastUpdated : Date
    isReviewed: Boolean,
    featuredPokemon: [String],
    variants: [String],
    additionalTags: [IAdditionalTag]
}

const cardSchema = new Schema({
    _id: { type: Schema.Types.ObjectId, required: true },
    cardInfo: { type: cardInfoSchema },
    lastUpdated: {type: Date},
    isReviewed: {type: Boolean, default: false},
    featuredPokemon: {type: [String]},
    variants: {type: [String]},
    additionalTags: {type: [additionalTagSchema]}
},
{
    collection: 'Cards',
    timestamps: true
})
cardSchema.index({cardInfo: 1, "cardInfo.artist": 1, "cardInfo.name" : 1});

export type Card = InferSchemaType<typeof cardSchema>;

// TODO: Change to "card"
export default model<Card>("Card", cardSchema);