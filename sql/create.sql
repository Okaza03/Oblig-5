-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema eventhub
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema eventhub
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `eventhub` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `eventhub` ;

-- -----------------------------------------------------
-- Table `eventhub`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eventhub`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(45) NULL DEFAULT NULL,
  `lastName` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `image` VARCHAR(45) NULL DEFAULT NULL,
  `email_verified` TINYINT(1) NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 103
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `eventhub`.`event`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eventhub`.`event` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  `date` DATETIME NULL DEFAULT NULL,
  `location` VARCHAR(45) NULL DEFAULT NULL,
  `image` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `user_id_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `event_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `eventhub`.`user` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 35
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `eventhub`.`event_has_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `eventhub`.`event_has_user` (
  `event_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`event_id`, `user_id`),
  INDEX `fk_event_has_user_user1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_event_has_user_event1_idx` (`event_id` ASC) VISIBLE,
  CONSTRAINT `fk_event_has_user_event1`
    FOREIGN KEY (`event_id`)
    REFERENCES `eventhub`.`event` (`id`),
  CONSTRAINT `fk_event_has_user_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `eventhub`.`user` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
