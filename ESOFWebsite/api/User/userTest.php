<?php
declare(strict_types=1);

use PHPUnit\Framework\TestCase;

final class userTest extends TestCase
{
    public function testCanBeCreatedFromValidEmailAddress(): void
    {
        $this->assertInstanceOf(
            signup::class,
            signup::fromString('user')
        );
    }

    public function testCannotBeCreatedFromInvalidEmailAddress(): void
    {
        $this->expectException(InvalidArgumentException::class);

        signup::fromString('invalid');
    }

    public function testCanBeUsedAsString(): void
    {
        $this->assertEquals(
            'user',
            signup::fromString('user')
        );
    }
}