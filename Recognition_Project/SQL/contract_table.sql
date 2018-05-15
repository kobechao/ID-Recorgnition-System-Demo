CREATE TABLE `DBO_BLOCKCHAIN`.`new_table` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `name` VARCHAR(20) NOT NULL,
      `contractAddress` VARCHAR(40) NOT NULL,
      `userToken` VARCHAR(40) NOT NULL,
      `contractABI` VARCHAR(400) NOT NULL,
      PRIMARY KEY (`id`, `name`),
      UNIQUE INDEX `id_UNIQUE` (`id` ASC),
      UNIQUE INDEX `name_UNIQUE` (`name` ASC));
