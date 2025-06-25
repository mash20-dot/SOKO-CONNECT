# SOKOCONNECT

SOKOCONNECT is a web platform that allows businesses to sign up, post their products, and connect with buyers. The goal is to help businesses showcase their products and make it easy for customers to browse, contact, and buy.

THESE ARE THE FEATURES:
- User registration and login (authentication, this entails the registration form for a buyer and a registration form for a business owner)
- Landing page(with a button to ask if the user is a business owner or a a buyer and a little info about the web page)
- User dashboard: this dashboard will be different according to the person signed up, either it's a buyer or a user.
- if it's a buyer the dashboard will contain a button taking the buyer to the feed, some list of businesses we have on the platform, and a search bar to search for a product and the buyer profile
- if it a business owner the dashboard will contain a button that will take the bussiner owner to his page where there will be a form if the bussiness owner wants to post products, the business owner can track how many buyers has contacted them so far and a button to view their own profile which will be available to the public
- on the feed will be products of our signed up businesses products which a buyer can click on and contact the business owner, a buyer can like and comment on the products
- There will also be a side bar where the customer can allow notifications, settings, and a logout option which will be in the settings option


PROJECT STRUCTURE:
├── client
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   │   └── vite.svg
│   ├── README.md
│   ├── src
│   │   ├── App.tsx
│   │   ├── assets
│   │   │   └── react.svg
│   │   ├── index.css
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
├── instance
└── server
    ├── app.py
    ├── instance
    │   └── sokoconnect.db
    └── requirements.txt

8 directories, 18 files

