-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `discowzoirmybb` DEFAULT CHARACTER SET utf8 ;
USE `discowzoirmybb` ;

-- -----------------------------------------------------
-- Table `discowzoirmybb`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `discowzoirmybb`.`user` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `pseudo` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `discowzoirmybb`.`score`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `discowzoirmybb`.`score` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` INT UNSIGNED NOT NULL,
  `score` INT UNSIGNED NOT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `course_type` ENUM('Q', 'QH', 'I') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `fk_score_user_idx` (`user_id` ASC),
  CONSTRAINT `fk_score_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `discowzoirmybb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `discowzoirmybb`.`session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `discowzoirmybb`.`session` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` INT UNSIGNED NOT NULL,
  `ip` VARCHAR(255) NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `fk_session_user1_idx` (`user_id` ASC),
  CONSTRAINT `fk_session_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `discowzoirmybb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;