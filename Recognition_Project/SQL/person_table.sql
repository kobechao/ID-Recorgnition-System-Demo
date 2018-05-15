CREATE TABLE `DBO_BLOCKCHAIN`.`personal_data` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `name` VARCHAR(45) NULL,
      `birthday` DATE NULL,
      `personalID` VARCHAR(10) NULL,
      `passportID` VARCHAR(10) NULL,
      `marrige` VARCHAR(10) NULL,
      `family` VARCHAR(10) NULL,
      `education` VARCHAR(10) NULL,
      `occupation` VARCHAR(10) NULL,
      PRIMARY KEY (`id`),
      UNIQUE INDEX `id_UNIQUE` (`id` ASC),
      UNIQUE INDEX `personalID_UNIQUE` (`personalID` ASC),
      UNIQUE INDEX `passportID_UNIQUE` (`passportID` ASC));
