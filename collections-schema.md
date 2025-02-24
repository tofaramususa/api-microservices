### folders database collections

{
  _id: ObjectId("..."),
  folderNumber: "FOLDER_001", //this is the one we show to users on the frontend
  name: "Cars", //name of the folder
  description:"This contains information about cars",
  products: [objectId], ///references to products 
  
  createdAt: ISODate("2025-02-17T13:41:26.000Z")
  updatedAt: ISODate("2025-02-17T13:41:26.000Z")
}

### products database collections

{
  _id: ObjectId,
  folderId: ObjectId,  // Reference to parent folder
  name: String,
  description: String,
  snapshots: [ObjectId], // References to snapshots
  #this below is for later
  accessControl: {
    ownerUserId: ObjectId,
    sharedWithUsers: [ObjectId],
    publicAccess: Boolean,
    accessLevel: String
  },
  createdAt: Date,
  updatedAt: Date
}

### snapshots database collections
const snapshotSchema = {
  _id: ObjectId,
  productId: ObjectId, // Reference to parent product
  version: String,
  timestamp: Date,
  contentPieces: [ObjectId], // this will be return for sure but for now only the share of voice
  //This will be removed but can be added later
  accessControl: {
    ownerUserId: ObjectId,
    sharedWithUsers: [ObjectId],
    publicAccess: Boolean,
    accessLevel: String
  },
  createdAt: Date,
  updatedAt: Date
}



## Share of Voice Raw Data collections Schema

## Share of Voice Report collections Schema

## Content Piece collections Schema














//May be needed wayyy later
// Users Collection
const userSchema = {
  _id: ObjectId,
  email: String,
  name: String,
  role: String,
  accessibleFolders: [ObjectId],  // References to folders this user can access
  accessibleProducts: [ObjectId], // References to products this user can access
  createdAt: Date,
  updatedAt: Date
}
