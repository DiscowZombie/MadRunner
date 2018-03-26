-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema madrunner
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema madrunner
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `madrunner` DEFAULT CHARACTER SET utf8 ;
USE `madrunner` ;

-- -----------------------------------------------------
-- Table `madrunner`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `madrunner`.`user` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `pseudo` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `madrunner`.`session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `madrunner`.`session` (
  `uuid` VARCHAR(255) NOT NULL,
  `user_id` INT UNSIGNED NOT NULL,
  `ip` VARCHAR(255) NOT NULL,
  `date` DATE NULL,
  PRIMARY KEY (`uuid`),
  UNIQUE INDEX `uuid_UNIQUE` (`uuid` ASC),
  INDEX `fk_session_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_session_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `madrunner`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `madrunner`.`score`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `madrunner`.`score` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` INT UNSIGNED NOT NULL,
  `score` INT UNSIGNED NOT NULL,
  `date` DATE NULL,
  `coursetype` ENUM('Q', 'QH', 'I') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `fk_score_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_score_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `madrunner`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


ALTER TABLE `session` CHANGE `date` `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP 
ALTER TABLE `score` CHANGE `date` `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP 

-- -----------------------------------------------------
-- Insert anonymous user into table
-- -----------------------------------------------------
INSERT INTO `madrunner`.`user` (
	`pseudo`, `password`
) VALUES ("Anonymous", "password");


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
