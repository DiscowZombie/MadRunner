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
  `id` INT(10) UNSIGNED NOT NULL,
  `pseudo` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `madrunner`.`session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `madrunner`.`session` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` INT(10) UNSIGNED NOT NULL,
  `uuid` VARCHAR(255) NOT NULL,
  `ip` VARCHAR(255) NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_session_user_idx` (`user_id` ASC),
  UNIQUE INDEX `uuid_UNIQUE` (`uuid` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
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
  `id` INT(10) UNSIGNED NOT NULL,
  `user_id` INT(10) UNSIGNED NOT NULL,
  `score` INT(16) UNSIGNED NOT NULL,
  `time` VARCHAR(255) NOT NULL,
  `difficulty` ENUM('F', 'M', 'D') NOT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `course_type` ENUM('Q', 'QH', 'I') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `fk_score_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_score_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `madrunner`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;