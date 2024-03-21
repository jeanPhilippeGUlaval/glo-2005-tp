CREATE TABLE color (colorId int PRIMARY KEY, colorName varchar(25));

CREATE TABLE porte (porteId int PRIMARY KEY, bundleID int FOREIGN KEY (bundleID) REFERENCES Bundle(bundleID));

CREATE TABLE bundle (bundleID int PRIMARY KEY, bundleName varchar(25));

CREATE TABLE bundle_asso_color (BundleID int, ColorID int, PRIMARY KEY (BundleID, ColorID), FOREIGN KEY (BundleID) REFERENCES Bundle(BundleID), FOREIGN KEY (ColorID) REFERENCES color(ColorID));

