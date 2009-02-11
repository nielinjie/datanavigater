CREATE TABLE "employee" (
    "id" INTEGER PRIMARY KEY NOT NULL,
    "name" TEXT NOT NULL,
    "managerId" INTEGER NOT NULL
    ,"companyId" integer not null
    ,constraint "employee_manager" foreign key (managerId) references "employee" (id)
    ,constraint "employee_company" foreign key (companyId) references "company" (id)
);

create table "company" (
    "id" integer primary key not null
    ,"name" text
);

CREATE TABLE address (
    "address" TEXT,
    "id" INTEGER,
    "employeeId" INTEGER
    , "countryId" INTEGER
    ,constraint "address_employee" foreign key (employeeId) references "employee" (id)
    ,constraint "address_country" foreign key (countryId) references "country" (id)
);

CREATE TABLE "country" (
    "id" INTEGER NOT NULL,
    "name" TEXT
);
